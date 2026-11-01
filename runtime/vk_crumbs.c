// GPU breadcrumbs for a lost device (vk.h vk_crumb). VK_AMD_buffer_marker writes a 32-bit code into a buffer from
// the command stream: at TOP_OF_PIPE once the command processor reaches the marker, at BOTTOM_OF_PIPE once every
// command before it has finished. Each crumb writes both, into two words of one host-coherent buffer, so after a
// device loss word 0 names the newest point the GPU reached and word 1 the newest point it had finished: the hang lies
// between them. A code is the crumb kind in the top 4 bits and its number in the low 28. The markers cost two small
// writes per crumb, and crumbs mark submissions, upload batches, ASTC chunks and presents; with TOTK_CRUMBS_OPS also
// every draw, dispatch and copy of the replay, into words 2 and 3 of their own.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "host.h"
#include "nvn_api.h"
#include "vk.h"

static PFN_vkCmdWriteBufferMarkerAMD write_marker;
static VkBuffer buf;
static VmaAllocation alloc;
static volatile uint32_t *words;

void vk_crumbs_init(VkCtx *c) {
    if (!c->has_buffer_marker) return;
    write_marker = (PFN_vkCmdWriteBufferMarkerAMD)vkGetDeviceProcAddr(c->device, "vkCmdWriteBufferMarkerAMD");
    VkBufferCreateInfo bi = {.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO, .size = 32,
                             .usage = VK_BUFFER_USAGE_TRANSFER_DST_BIT};
    VmaAllocationCreateInfo ai = {.usage = VMA_MEMORY_USAGE_AUTO_PREFER_HOST,
                                  .flags = VMA_ALLOCATION_CREATE_HOST_ACCESS_RANDOM_BIT | VMA_ALLOCATION_CREATE_MAPPED_BIT,
                                  .requiredFlags = VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT};
    VmaAllocationInfo info;
    if (!write_marker || vmaCreateBuffer(c->vma, &bi, &ai, &buf, &alloc, &info) != VK_SUCCESS) {
        rt_log("vk: GPU breadcrumbs unavailable");
        write_marker = NULL;
        return;
    }
    words = info.pMappedData;
    for (int i = 0; i < 8; i++) words[i] = 0;
    rt_log("vk: GPU breadcrumbs on (VK_AMD_buffer_marker)");
}

void vk_crumbs_release(void) {
    VkCtx *c = vk_ctx();
    if (buf && c) vmaDestroyBuffer(c->vma, buf, alloc);
    buf = VK_NULL_HANDLE, alloc = NULL, words = NULL, write_marker = NULL;
}

void vk_crumb(VkCommandBuffer cb, int kind, uint64_t n) {
    if (!write_marker || !cb) return;
    uint32_t code = (uint32_t)kind << 28 | (uint32_t)(n & 0x0fffffff);
    // op crumbs keep words 2 and 3 and present steps words 4 and 5: other submissions would overwrite them
    VkDeviceSize at = kind == VK_CRUMB_OP ? 8 : kind == VK_CRUMB_PRESENT_STEP ? 16 : 0;
    write_marker(cb, VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT, buf, at, code);
    write_marker(cb, VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT, buf, at + 4, code);
}

// ---- per-op crumbs (TOTK_CRUMBS_OPS)
enum { OPS_RING = 1 << 16 };
enum { OP_PASS_END = -1, OP_PASS_BEGIN = -2 };   // op crumbs around vkCmdBeginRendering / EndRendering, not NVN ops
typedef struct { uint32_t n; int op; uint64_t prog; uint8_t vs[4], fs[4]; int prim; int32_t count; VkCrumbTex tex; } OpCrumb;   // vs, fs: key prefixes
static OpCrumb ops[OPS_RING];
static uint32_t ops_n;   // the last op crumb's number (the replay is one thread)

int vk_crumbs_ops_on(void) {
    static int on = -1;
    if (on < 0) {
        on = write_marker && rt_knob("CRUMBS_OPS", "0");
        if (on) rt_log("vk: GPU breadcrumbs before every draw, dispatch and copy (TOTK_CRUMBS_OPS)");
    }
    return on;
}

void vk_crumb_op(VkCommandBuffer cb, int op, uint64_t prog) {
    uint32_t n = ++ops_n & 0x0fffffff;
    ops[n % OPS_RING] = (OpCrumb){n, op, prog};
    rec_drain();   // the recorder made every call before this one: the marker lands in order
    vk_crumb(cb, VK_CRUMB_OP, n);
}

// Names the shaders (gfx_shader_key prefixes, as in the translator's cache) and the size of the draw the last op
// crumb marks: a program serial is new at every run, a shader key is not.
void vk_crumb_op_draw(const uint8_t *vs_key, const uint8_t *fs_key, int prim, int32_t count, const VkCrumbTex *tex) {
    OpCrumb *o = &ops[ops_n % OPS_RING];
    if (vs_key) memcpy(o->vs, vs_key, 4);
    if (fs_key) memcpy(o->fs, fs_key, 4);
    o->prim = prim, o->count = count, o->tex = *tex;
}

void vk_crumb_pass_begin(VkCommandBuffer cb) {
    if (vk_crumbs_ops_on()) vk_crumb_op(cb, OP_PASS_BEGIN, 0);
}

void vk_crumb_pass_end(VkCommandBuffer cb) {
    if (vk_crumbs_ops_on()) vk_crumb_op(cb, OP_PASS_END, 0);
}

static void op_log(const char *what, uint32_t n) {
    const OpCrumb *o = &ops[n % OPS_RING];
    if (o->n != n) { rt_log("vk:   %s op %u (no longer in the ring)", what, n); return; }
    if (o->op < 0) {
        rt_log("vk:   %s op %u: the %s of a render pass", what, n, o->op == OP_PASS_END ? "end" : "beginning");
        return;
    }
    if (!o->count) {
        rt_log("vk:   %s op %u: %s, program %llu", what, n, nvn_op_name(o->op), (unsigned long long)o->prog);
        return;
    }
    rt_log("vk:   %s op %u: %s, program %llu, vs %02x%02x%02x%02x fs %02x%02x%02x%02x, primitive %d, %d vertices", what, n,
           nvn_op_name(o->op), (unsigned long long)o->prog, o->vs[0], o->vs[1], o->vs[2], o->vs[3], o->fs[0], o->fs[1],
           o->fs[2], o->fs[3], o->prim, o->count);
    const VkCrumbTex *t = &o->tex;
    if (t->found)
        rt_log("vk:     its fragment shader's first texture: handle %#llx (type %#x), VkFormat %u, %ux%u, %u layers, "
               "%u levels, storage %#llx", (unsigned long long)t->handle, t->type, t->format, t->w, t->h, t->layers,
               t->levels, (unsigned long long)t->addr);
    else if (t->type)
        rt_log("vk:     its fragment shader's first texture: handle %#llx (type %#x) has no image (a stand-in is bound)",
               (unsigned long long)t->handle, t->type);
}

static void describe(uint32_t code, char *o, size_t size) {
    static const char *const kinds[] = {"nothing", "the start of a part of submission", "the end of submission",
                                        "the start of upload batch", "the end of upload batch",
                                        "ASTC decode chunk", "the start of present",
                                        "the end of present", "replay op", "present step"};
    unsigned k = code >> 28;
    if (!code) snprintf(o, size, "nothing yet");
    else if (k < sizeof kinds / sizeof *kinds) snprintf(o, size, "%s %u", kinds[k], code & 0x0fffffff);
    else snprintf(o, size, "unknown code %#x", code);
}

void vk_crumbs_report(void) {
    if (!words) return;
    char reached[96], finished[96];
    describe(words[0], reached, sizeof reached);
    describe(words[1], finished, sizeof finished);
    rt_log("vk: GPU breadcrumbs: the GPU last reached %s; everything before %s had finished", reached, finished);
    static const char *const steps[] = {"?", "its start", "the colour adjustment", "the scaling (FSR or blit)",
                                        "the menu overlay", "the copies (capture, thumbnail)"};
    uint32_t pr = words[4] & 0x0fffffff, pf = words[5] & 0x0fffffff;
    if (pr) rt_log("vk: GPU breadcrumbs of the present of frame %u: reached the step after %s; frame %u had finished the "
                   "step after %s", pr >> 3, steps[(pr & 7) < 6 ? (pr & 7) : 0], pf >> 3, steps[(pf & 7) < 6 ? (pf & 7) : 0]);
    uint32_t r = words[2], f = words[3];
    if (r) rt_log("vk: GPU breadcrumbs of the replay: reached op %u, everything before op %u had finished",
                  r & 0x0fffffff, f & 0x0fffffff);
    if (r >> 28 == VK_CRUMB_OP && f >> 28 == VK_CRUMB_OP) {   // the hang lies from the op after f up to r
        uint32_t a = (f & 0x0fffffff) + 1, b = r & 0x0fffffff;
        for (uint32_t i = a > 6 ? a - 6 : 1; i < a; i++) op_log("before", i);   // what led up to it
        if (b >= a && b - a < 16) for (uint32_t i = a; i <= b; i++) op_log(i == b ? "reached" : "running", i);
        else op_log("finished", f & 0x0fffffff), op_log("reached", b);
    } else if (r >> 28 == VK_CRUMB_OP) op_log("reached", r & 0x0fffffff);
}

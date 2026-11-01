// NVN 53 procs that Super Mario Odyssey (SDK 7.3.2) loads and TotK's NVN 55 no longer has. nvn_procs.c registers
// them only for SMO builds (RT_SMO), so a TotK build resolves the same names as before.
#include "host.h"

void nvnp_nvnWindowAcquireTexture(Cpu *c);

// void nvnQueueAcquireTexture(NVNqueue *q, NVNwindow *w, int *index): NVN 53's acquire, before the window took a
// sync object. The queue only ordered the acquire against its earlier work; presents are copies queued in submit
// order (nvn_api_obj.c nvnWindowAcquireTexture), so it is the window acquire without a sync.
void nvnp_nvnQueueAcquireTexture(Cpu *c) {
    c->x[0] = c->x[1];
    c->x[1] = 0;
    nvnp_nvnWindowAcquireTexture(c);
}

// void nvnDeviceApplyDeferredFinalizes(NVNdevice *d, int age): objects finalize at once here, so nothing is deferred.
void nvnp_nvnDeviceApplyDeferredFinalizes(Cpu *c) { (void)c; }

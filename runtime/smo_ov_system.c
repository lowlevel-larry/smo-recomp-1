// Host overrides of system functions only Super Mario Odyssey (SDK 7.3.2) imports. Each symbol is absent from TotK's
// modules, so a TotK build binds none of them.
#include <stdint.h>
#include <string.h>

#include "host.h"
#include "platform/platform.h"

// nn::settings::Language -> LanguageCode (an 8-byte NUL-padded string), the table of set:MakeLanguageCode
// (Switchbrew "Settings services").
static const char *const language_codes[] = {
    "ja", "en-US", "fr", "de", "it", "es", "zh-CN", "ko", "nl", "pt", "ru", "zh-TW", "en-GB", "fr-CA", "es-419",
    "zh-Hans", "zh-Hant", "pt-BR",
};

// bool nn::settings::operator==(const LanguageCode &code, const Language &language): the SDK builds the language's
// code through the "set" service, which this runtime does not host; the table gives the same code.
static void ov_language_code_equal(Cpu *c) {
    const char *code = arg_p(c, 0);
    int32_t language;
    memcpy(&language, arg_p(c, 1), 4);
    char want[8] = {0};
    if (language >= 0 && language < (int32_t)(sizeof language_codes / sizeof *language_codes))
        strncpy(want, language_codes[language], sizeof want);
    ret_x(c, want[0] && !memcmp(code, want, sizeof want));
}
HOST_OVERRIDE("_ZN2nn8settingseqERKNS0_12LanguageCodeERKNS0_8LanguageE", ov_language_code_equal);

// ---- nn::account beyond TotK's set. ov_system.c replaces account::Initialize without opening the account service,
// so the functions SMO adds answer from the local account too.
void account_uid(uint64_t out[2]);   // ov_system.c: the local account's Uid

// nn::Result GetLastOpenedUser(Uid *out): the local account
static void ov_last_opened_user(Cpu *c) {
    uint64_t uid[2];
    account_uid(uid);
    memcpy(arg_p(c, 0), uid, sizeof uid);
    ret_x(c, 0);
}
HOST_OVERRIDE("_ZN2nn7account17GetLastOpenedUserEPNS0_3UidE", ov_last_opened_user);

// nn::Result IsNetworkServiceAccountAvailable(bool *out, const UserHandle &): offline, no Nintendo Account link
static void ov_nsa_available(Cpu *c) {
    *(uint8_t *)arg_p(c, 0) = 0;
    ret_x(c, 0);
}
HOST_OVERRIDE("_ZN2nn7account32IsNetworkServiceAccountAvailableEPbRKNS0_10UserHandleE", ov_nsa_available);

// ---- nn::fs names of SDK 7.3.2 that fs_host.c knows under its SDK 20 names
// nn::Result EnsureSaveData(const Uid &): fs_host.c creates the save directory on first mount, as the launcher does
static void ov_ensure_save_data(Cpu *c) { ret_x(c, 0); }
HOST_OVERRIDE("_ZN2nn2fs14EnsureSaveDataERKNS_7account3UidE", ov_ensure_save_data);

// nn::Result CommitSaveData(const char *mount): SDK 20's Commit(const char *)
static void ov_commit_save_data(Cpu *c) {
    GuestFn commit = hostfn_override("_ZN2nn2fs6CommitEPKc");
    if (!commit) rt_fatal("nn::fs::CommitSaveData: no host Commit");
    commit(c);
}
HOST_OVERRIDE("_ZN2nn2fs14CommitSaveDataEPKc", ov_commit_save_data);

// ---- nn::oe and nn::account functions SMO calls under SDK 7 names
int32_t ov_performance_configuration(int mode);   // ov_system.c: the configuration last set for that mode

// int nn::oe::GetPerformanceConfiguration(PerformanceMode mode)
static void ov_get_performance_config(Cpu *c) {
    int64_t mode = (int32_t)arg_x(c, 0);
    if (mode < 0 || mode > 1) rt_fatal("nn::oe::GetPerformanceConfiguration: invalid mode %lld", (long long)mode);
    ret_x(c, (uint32_t)ov_performance_configuration((int)mode));
}
HOST_OVERRIDE("_ZN2nn2oe27GetPerformanceConfigurationENS0_15PerformanceModeE", ov_get_performance_config);

// void nn::account::OpenPreselectedUser(UserHandle *): the aborting form of TryOpenPreselectedUser (ov_system.c),
// which always opens the local account
static void ov_open_preselected_user(Cpu *c) {
    GuestFn open = hostfn_override("_ZN2nn7account22TryOpenPreselectedUserEPNS0_10UserHandleE");
    if (!open) rt_fatal("nn::account::OpenPreselectedUser: no host TryOpenPreselectedUser");
    open(c);
}
HOST_OVERRIDE("_ZN2nn7account19OpenPreselectedUserEPNS0_10UserHandleE", ov_open_preselected_user);

// ---- nn::oe, nn::vi and nn::err calls of SMO without a TotK counterpart: system UI and capture settings that a host
// window has no use for.
static void ov_none(Cpu *c) { (void)c; }
static void ov_zero(Cpu *c) { ret_x(c, 0); }
// void SetScreenShotImageOrientation(album::ImageOrientation): the console's screenshot button; none here
HOST_OVERRIDE("_ZN2nn2oe29SetScreenShotImageOrientationENS_5album16ImageOrientationE", ov_none);
// void EnableRecording() / DisableRecording(): video capture allowed or not
HOST_OVERRIDE("_ZN2nn2oe15EnableRecordingEv", ov_none);
HOST_OVERRIDE("_ZN2nn2oe16DisableRecordingEv", ov_none);
// void BeginBlockingHomeButton() / EndBlockingHomeButton(): the HOME menu, which does not exist here
HOST_OVERRIDE("_ZN2nn2oe23BeginBlockingHomeButtonEv", ov_none);
HOST_OVERRIDE("_ZN2nn2oe21EndBlockingHomeButtonEv", ov_none);
// bool IsUserInactivityDetectionTimeExtended(): the console's auto-sleep timer is never extended here
HOST_OVERRIDE("_ZN2nn2oe37IsUserInactivityDetectionTimeExtendedEv", ov_zero);
// nn::Result vi::SetLayerScalingMode(Layer *, ScalingMode): the swapchain scales the frame (gfx_window_sdl.c)
HOST_OVERRIDE("_ZN2nn2vi19SetLayerScalingModeEPNS0_5LayerENS0_11ScalingModeE", ov_zero);
// void err::ReportMultimediaError(Result, const movie::MultimediaTelemetryReport &): telemetry of the movie player
HOST_OVERRIDE("_ZN2nn3err21ReportMultimediaErrorENS_6ResultERKN5movie25MultimediaTelemetryReportE", ov_none);

// ---- diagnostics
// bool nn::diag::IsDebuggerAttached(): SMO asks it in its heap's allocation-failure callback (main+0x97bfa0), which
// traps when it is false. The callback's argument (x1, untouched until here) is {heap, size, alignment, ...}:
// log it so an out-of-memory stop names the heap and the request.
static void ob_debugger_attached(Cpu *c) {
    uint64_t lr = c->x[30], info = c->x[1];
    const RtLoaded *m = ldr_count() ? ldr_module(0) : NULL;
    if (m && lr - m->base == 0x97bfac && plat_mem_readable(info, 0x28)) {
        uint64_t heap = LD64(info), size = LD64(info + 8);
        uint32_t align = LD32(info + 0x10);
        rt_log("smo: allocation failed: heap %#llx, %#llx bytes (%.1f MiB), alignment %u",
               (unsigned long long)heap, (unsigned long long)size, size / 1048576.0, align);
        if (plat_mem_readable(heap, 0x100))
            for (int i = 0; i < 0x100; i += 0x40)
                rt_log("smo:   heap+%#x: %016llx %016llx %016llx %016llx %016llx %016llx %016llx %016llx", i,
                       (unsigned long long)LD64(heap + i), (unsigned long long)LD64(heap + i + 8),
                       (unsigned long long)LD64(heap + i + 16), (unsigned long long)LD64(heap + i + 24),
                       (unsigned long long)LD64(heap + i + 32), (unsigned long long)LD64(heap + i + 40),
                       (unsigned long long)LD64(heap + i + 48), (unsigned long long)LD64(heap + i + 56));
    }
    rt_original(c);
}
HOST_OBSERVER("_ZN2nn4diag18IsDebuggerAttachedEv", ob_debugger_attached);

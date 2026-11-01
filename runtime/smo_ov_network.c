// Super Mario Odyssey's online and system-applet services, answered as an offline console: the libraries initialise,
// the network is never available, and the parental-control VR restriction is off. Each function logs its first call.
// None of these symbols is in TotK's modules (TotK's prepo and pctl overrides are in ov_system.c).
#include <stdint.h>

#include "host.h"
#include "platform/platform.h"

#define FIRST_CALL(what)                                                                                             \
    do {                                                                                                             \
        static volatile int32_t seen;                                                                                \
        if (!plat_xchg32(&seen, 1)) rt_log("offline: %s", what);                                                     \
    } while (0)

// nn::Result values these functions return when the service would need the network: <module, description 1>.
#define RESULT_NIFM_UNAVAILABLE (110u | 1u << 9)
#define RESULT_BCAT_UNAVAILABLE (122u | 1u << 9)



static void ov_friends_initialize(Cpu *c) { FIRST_CALL("nn::friends::Initialize"); (void)c; }
HOST_OVERRIDE("_ZN2nn7friends10InitializeEv", ov_friends_initialize);

static void ov_nifm_initialize(Cpu *c) { FIRST_CALL("nn::nifm::Initialize"); ret_x(c, 0); }
static void ov_nifm_submit(Cpu *c) { FIRST_CALL("nn::nifm::SubmitNetworkRequest"); (void)c; }
static void ov_false(Cpu *c) { ret_x(c, 0); }
static void ov_nifm_handle(Cpu *c) { FIRST_CALL("nn::nifm::HandleNetworkRequestResult: offline"); ret_x(c, RESULT_NIFM_UNAVAILABLE); }
static void ov_nifm_address(Cpu *c) { ret_x(c, RESULT_NIFM_UNAVAILABLE); }
HOST_OVERRIDE("_ZN2nn4nifm10InitializeEv", ov_nifm_initialize);
HOST_OVERRIDE("_ZN2nn4nifm20SubmitNetworkRequestEv", ov_nifm_submit);
HOST_OVERRIDE("_ZN2nn4nifm27SubmitNetworkRequestAndWaitEv", ov_nifm_submit);
HOST_OVERRIDE("_ZN2nn4nifm18IsNetworkAvailableEv", ov_false);
HOST_OVERRIDE("_ZN2nn4nifm22IsNetworkRequestOnHoldEv", ov_false);
HOST_OVERRIDE("_ZN2nn4nifm26HandleNetworkRequestResultEv", ov_nifm_handle);
HOST_OVERRIDE("_ZN2nn4nifm26GetCurrentPrimaryIpAddressEP7in_addr", ov_nifm_address);
HOST_OVERRIDE("_ZN2nn4nifm22GetCurrentProxySettingEPNS0_12ProxySettingE", ov_nifm_address);

// BCAT (news and event data delivered in the background): nothing was ever delivered.
static void ov_bcat_initialize(Cpu *c) { FIRST_CALL("nn::bcat::Initialize"); (void)c; }
static void ov_bcat_mount(Cpu *c) { FIRST_CALL("nn::bcat::MountDeliveryCacheStorage: nothing delivered"); ret_x(c, RESULT_BCAT_UNAVAILABLE); }
static void ov_bcat_unmount(Cpu *c) { (void)c; }
HOST_OVERRIDE("_ZN2nn4bcat10InitializeEv", ov_bcat_initialize);
HOST_OVERRIDE("_ZN2nn4bcat25MountDeliveryCacheStorageEv", ov_bcat_mount);
HOST_OVERRIDE("_ZN2nn4bcat27UnmountDeliveryCacheStorageEv", ov_bcat_unmount);
HOST_OVERRIDE("_ZN2nn4bcat24RequestSyncDeliveryCacheEPNS0_21DeliveryCacheProgressE", ov_bcat_mount);

// Parental controls of the Labo VR mode: no restriction, and the setting is not configurable here.
static void ov_ok(Cpu *c) { ret_x(c, 0); }
static void ov_nothing(Cpu *c) { (void)c; }
HOST_OVERRIDE("_ZN2nn4pctl26GetStereoVisionRestrictionEv", ov_false);
HOST_OVERRIDE("_ZN2nn4pctl26SetStereoVisionRestrictionEb", ov_nothing);
HOST_OVERRIDE("_ZN2nn4pctl42ConfirmStereoVisionRestrictionConfigurableEv", ov_ok);
HOST_OVERRIDE("_ZN2nn4pctl53RequestStereoVisionRestrictionConfigurationPermissionEv", ov_ok);

// Play reports (telemetry): built and dropped; ov_system.c already drops Save.
HOST_OVERRIDE("_ZN2nn5prepo10PlayReportC1EPKc", ov_nothing);
HOST_OVERRIDE("_ZN2nn5prepo10PlayReport9SetBufferEPvm", ov_ok);
HOST_OVERRIDE("_ZN2nn5prepo10PlayReport3AddEPKcl", ov_ok);
HOST_OVERRIDE("_ZN2nn5prepo10PlayReport3AddEPKcd", ov_ok);
HOST_OVERRIDE("_ZN2nn5prepo10PlayReport3AddEPKcRKNS0_10Any64BitIdE", ov_ok);

// Sockets: the library initialises; nothing connects while the network is unavailable.
static void ov_socket_initialize(Cpu *c) { FIRST_CALL("nn::socket::Initialize"); ret_x(c, 0); }
HOST_OVERRIDE("_ZN2nn6socket10InitializeEPvmmi", ov_socket_initialize);

// SSL (NEX and libcurl): the library initialises; no connection is made while the network is unavailable.
static void ov_ssl_initialize(Cpu *c) { FIRST_CALL("nn::ssl::Initialize"); ret_x(c, 0); }
HOST_OVERRIDE("nnsslInitialize", ov_ssl_initialize);
HOST_OVERRIDE("_ZN2nn3ssl10InitializeEv", ov_ssl_initialize);

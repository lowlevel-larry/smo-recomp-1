# Inventário nn:: do SMO 1.4.1 (SDK 7.3.2) vs HOST_OVERRIDE do runtime

Gerado por `tools/smo_sdk_gap.py`. "tem": override com o mesmo símbolo; "assinatura difere": override para o mesmo nome qualificado com outra assinatura (SDK 20 do TotK), candidato a adaptar; "falta": nenhum override, roda o código do próprio `sdk` do jogo (o padrão; só vira trabalho se esse código precisar de serviço do Horizon que o runtime não emula).

- Imports nn:: dos módulos: 566 (tem 122, assinatura difere 0, falta 444)
- Overrides do runtime: 215; sem referência em nenhum módulo do SMO: 3
- Imports não-nn (libc, NVN, etc.): 728

## Por namespace

| Namespace | tem | assinatura difere | falta |
|---|---|---|---|
| `nn::audio` | 0 | 0 | 106 |
| `nn::os` | 0 | 0 | 69 |
| `nn::hid` | 23 | 0 | 26 |
| `nn::socket` | 1 | 0 | 26 |
| `nn::fontll` | 0 | 0 | 24 |
| `nn::oe` | 16 | 0 | 7 |
| `nn::util` | 0 | 0 | 22 |
| `nn::fs` | 21 | 0 | 0 |
| `nn::account` | 7 | 0 | 10 |
| `nn::bcat` | 4 | 0 | 13 |
| `nn::diag` | 0 | 0 | 14 |
| `nn::nfp` | 12 | 0 | 1 |
| `nn::sf` | 0 | 0 | 11 |
| `nn::mem` | 0 | 0 | 9 |
| `nn::nifm` | 8 | 0 | 0 |
| `nn::web` | 0 | 0 | 8 |
| `nn::friends` | 1 | 0 | 5 |
| `nn::prepo` | 6 | 0 | 0 |
| `nn::swkbd` | 1 | 0 | 5 |
| `nn::time` | 6 | 0 | 0 |
| `nn::vi` | 5 | 0 | 1 |
| `nn::lmem` | 0 | 0 | 6 |
| `nn::pl` | 3 | 0 | 2 |
| `nn::crypto` | 0 | 0 | 5 |
| `nn::image` | 0 | 0 | 5 |
| `nn::pctl` | 4 | 0 | 0 |
| `nn::err` | 1 | 0 | 1 |
| `nn::ssl` | 0 | 0 | 2 |
| `nn::settings` | 1 | 0 | 0 |
| `nnsslInitialize` | 1 | 0 | 0 |
| `void nn::hid` | 1 | 0 | 0 |
| `nn::detail` | 0 | 0 | 1 |
| `nn::nsd` | 0 | 0 | 1 |
| `nnMain` | 0 | 0 | 1 |
| `nnResultGetDescription` | 0 | 0 | 1 |
| `nnResultGetModule` | 0 | 0 | 1 |
| `nnResultIsFailure` | 0 | 0 | 1 |
| `nnResultIsSuccess` | 0 | 0 | 1 |
| `nndetailDiagAbortFormatImpl` | 0 | 0 | 1 |
| `nninitStartup` | 0 | 0 | 1 |
| `nnosConvertTickToNanoSeconds` | 0 | 0 | 1 |
| `nnosCreateThread` | 0 | 0 | 1 |
| `nnosDestroyThread` | 0 | 0 | 1 |
| `nnosFinalizeEvent` | 0 | 0 | 1 |
| `nnosFinalizeMutex` | 0 | 0 | 1 |
| `nnosGetCurrentThread` | 0 | 0 | 1 |
| `nnosGetDefaultUserExceptionStackForApplication` | 0 | 0 | 1 |
| `nnosGetSystemTick` | 0 | 0 | 1 |
| `nnosGetSystemTickFrequency` | 0 | 0 | 1 |
| `nnosGetThreadCoreMask` | 0 | 0 | 1 |
| `nnosGetThreadPriority` | 0 | 0 | 1 |
| `nnosInitializeEvent` | 0 | 0 | 1 |
| `nnosInitializeMutex` | 0 | 0 | 1 |
| `nnosLockMutex` | 0 | 0 | 1 |
| `nnosSetThreadCoreMask` | 0 | 0 | 1 |
| `nnosSetThreadNamePointer` | 0 | 0 | 1 |
| `nnosSignalEvent` | 0 | 0 | 1 |
| `nnosSleepThread` | 0 | 0 | 1 |
| `nnosStartThread` | 0 | 0 | 1 |
| `nnosUnlockMutex` | 0 | 0 | 1 |
| `nnosWaitEvent` | 0 | 0 | 1 |
| `nnosWaitThread` | 0 | 0 | 1 |
| `nnsocketBind` | 0 | 0 | 1 |
| `nnsocketClose` | 0 | 0 | 1 |
| `nnsocketConnect` | 0 | 0 | 1 |
| `nnsocketFcntl` | 0 | 0 | 1 |
| `nnsocketGetHostByNameWithOptions` | 0 | 0 | 1 |
| `nnsocketGetLastErrno` | 0 | 0 | 1 |
| `nnsocketGetPeerName` | 0 | 0 | 1 |
| `nnsocketGetSockName` | 0 | 0 | 1 |
| `nnsocketGetSockOpt` | 0 | 0 | 1 |
| `nnsocketInetHtons` | 0 | 0 | 1 |
| `nnsocketInetNtohs` | 0 | 0 | 1 |
| `nnsocketPoll` | 0 | 0 | 1 |
| `nnsocketRecv` | 0 | 0 | 1 |
| `nnsocketResolverGetOption` | 0 | 0 | 1 |
| `nnsocketResolverSetOption` | 0 | 0 | 1 |
| `nnsocketSend` | 0 | 0 | 1 |
| `nnsocketSetLastErrno` | 0 | 0 | 1 |
| `nnsocketSetSockOpt` | 0 | 0 | 1 |
| `nnsocketSocket` | 0 | 0 | 1 |
| `nnsslConnectionCreate` | 0 | 0 | 1 |
| `nnsslConnectionDestroy` | 0 | 0 | 1 |
| `nnsslConnectionDoHandshakeWithCertBuffer` | 0 | 0 | 1 |
| `nnsslConnectionGetConnectionId` | 0 | 0 | 1 |
| `nnsslConnectionGetVerifyCertError` | 0 | 0 | 1 |
| `nnsslConnectionPending` | 0 | 0 | 1 |
| `nnsslConnectionRead` | 0 | 0 | 1 |
| `nnsslConnectionSetHostName` | 0 | 0 | 1 |
| `nnsslConnectionSetIoMode` | 0 | 0 | 1 |
| `nnsslConnectionSetOption` | 0 | 0 | 1 |
| `nnsslConnectionSetSessionCacheMode` | 0 | 0 | 1 |
| `nnsslConnectionSetSocketDescriptor` | 0 | 0 | 1 |
| `nnsslConnectionSetVerifyOption` | 0 | 0 | 1 |
| `nnsslConnectionWrite` | 0 | 0 | 1 |
| `nnsslContextDestroy` | 0 | 0 | 1 |
| `nnsslContextGetContextId` | 0 | 0 | 1 |

## Tem

| Símbolo | Override |
|---|---|
| `nn::account::CloseUser(nn::account::UserHandle const&)` | `ov_close_user` (runtime/ov_system.c) |
| `nn::account::GetLastOpenedUser(nn::account::Uid*)` | `ov_last_opened_user` (runtime/smo_ov_system.c) |
| `nn::account::GetNickname(nn::account::Nickname*, nn::account::Uid const&)` | `ov_nickname` (runtime/ov_system.c) |
| `nn::account::GetUserId(nn::account::Uid*, nn::account::UserHandle const&)` | `ov_user_id` (runtime/ov_system.c) |
| `nn::account::Initialize()` | `ov_account_initialize` (runtime/ov_system.c) |
| `nn::account::IsNetworkServiceAccountAvailable(bool*, nn::account::UserHandle const&)` | `ov_nsa_available` (runtime/smo_ov_system.c) |
| `nn::account::OpenPreselectedUser(nn::account::UserHandle*)` | `ov_open_user` (runtime/ov_system.c) |
| `nn::bcat::Initialize()` | `ov_bcat_initialize` (runtime/smo_ov_network.c) |
| `nn::bcat::MountDeliveryCacheStorage()` | `ov_bcat_mount` (runtime/smo_ov_network.c) |
| `nn::bcat::RequestSyncDeliveryCache(nn::bcat::DeliveryCacheProgress*)` | `ov_bcat_mount` (runtime/smo_ov_network.c) |
| `nn::bcat::UnmountDeliveryCacheStorage()` | `ov_bcat_unmount` (runtime/smo_ov_network.c) |
| `nn::err::ShowError(nn::Result)` | `ov_show_error` (runtime/ov_system.c) |
| `nn::friends::Initialize()` | `ov_friends_initialize` (runtime/smo_ov_network.c) |
| `nn::fs::CloseDirectory(nn::fs::DirectoryHandle)` | `ov_close_directory` (runtime/fs_host.c) |
| `nn::fs::CloseFile(nn::fs::FileHandle)` | `ov_close_file` (runtime/fs_host.c) |
| `nn::fs::CommitSaveData(char const*)` | `ov_commit_save_data` (runtime/smo_ov_system.c) |
| `nn::fs::CreateDirectory(char const*)` | `ov_create_directory` (runtime/fs_host.c) |
| `nn::fs::CreateFile(char const*, long)` | `ov_create_file` (runtime/fs_host.c) |
| `nn::fs::DeleteFile(char const*)` | `ov_delete_file` (runtime/fs_host.c) |
| `nn::fs::EnsureSaveData(nn::account::Uid const&)` | `ov_ensure_save_data` (runtime/smo_ov_system.c) |
| `nn::fs::FlushFile(nn::fs::FileHandle)` | `ov_flush_file` (runtime/fs_host.c) |
| `nn::fs::GetEntryType(nn::fs::DirectoryEntryType*, char const*)` | `ov_entry_type` (runtime/fs_host.c) |
| `nn::fs::GetFileSize(long*, nn::fs::FileHandle)` | `ov_file_size` (runtime/fs_host.c) |
| `nn::fs::MountRom(char const*, void*, unsigned long)` | `ov_mount_rom` (runtime/romfs.c) |
| `nn::fs::MountSaveData(char const*, nn::account::Uid const&)` | `ov_mount_save` (runtime/fs_host.c) |
| `nn::fs::OpenDirectory(nn::fs::DirectoryHandle*, char const*, int)` | `ov_open_directory` (runtime/fs_host.c) |
| `nn::fs::OpenFile(nn::fs::FileHandle*, char const*, int)` | `ov_open_file` (runtime/fs_host.c) |
| `nn::fs::QueryMountRomCacheSize(unsigned long*)` | `ov_query_cache` (runtime/romfs.c) |
| `nn::fs::ReadDirectory(long*, nn::fs::DirectoryEntry*, nn::fs::DirectoryHandle, long)` | `ov_read_directory` (runtime/fs_host.c) |
| `nn::fs::ReadFile(unsigned long*, nn::fs::FileHandle, long, void*, unsigned long)` | `ov_read_file` (runtime/fs_host.c) |
| `nn::fs::ReadFile(unsigned long*, nn::fs::FileHandle, long, void*, unsigned long, nn::fs::ReadOption const&)` | `ov_read_options` (runtime/fs_host.c) |
| `nn::fs::SetFileSize(nn::fs::FileHandle, long)` | `ov_set_file_size` (runtime/fs_host.c) |
| `nn::fs::Unmount(char const*)` | `ov_unmount` (runtime/fs_host.c) |
| `nn::fs::WriteFile(nn::fs::FileHandle, long, void const*, unsigned long, nn::fs::WriteOption const&)` | `ov_write_file` (runtime/fs_host.c) |
| `nn::hid::FinalizeSevenSixAxisSensor()` | `ov_result_ok` (runtime/smo_ov_input.c) |
| `nn::hid::GetDebugPadState(nn::hid::DebugPadState*)` | `ov_debug_pad_state` (runtime/smo_ov_input.c) |
| `nn::hid::GetNpadStates(nn::hid::NpadFullKeyState*, int, unsigned int const&)` | `ov_states_full_key` (runtime/ov_input.c) |
| `nn::hid::GetNpadStates(nn::hid::NpadHandheldState*, int, unsigned int const&)` | `ov_states_handheld` (runtime/ov_input.c) |
| `nn::hid::GetNpadStates(nn::hid::NpadJoyDualState*, int, unsigned int const&)` | `ov_states_joycon` (runtime/ov_input.c) |
| `nn::hid::GetNpadStates(nn::hid::NpadJoyLeftState*, int, unsigned int const&)` | `ov_states_joycon` (runtime/ov_input.c) |
| `nn::hid::GetNpadStates(nn::hid::NpadJoyRightState*, int, unsigned int const&)` | `ov_states_joycon` (runtime/ov_input.c) |
| `nn::hid::GetNpadStyleSet(unsigned int const&)` | `ov_style_set` (runtime/ov_input.c) |
| `nn::hid::GetSevenSixAxisSensorStates(nn::hid::SevenSixAxisSensorState*, int)` | `ov_seven_states` (runtime/smo_ov_input.c) |
| `nn::hid::InitializeDebugPad()` | `ov_nothing` (runtime/smo_ov_input.c) |
| `nn::hid::InitializeNpad()` | `ov_initialize_npad` (runtime/ov_input.c) |
| `nn::hid::InitializeSevenSixAxisSensor(void*, unsigned long)` | `ov_result_ok` (runtime/smo_ov_input.c) |
| `nn::hid::InitializeTouchScreen()` | `ov_nothing` (runtime/smo_ov_input.c) |
| `nn::hid::IsSevenSixAxisSensorAtRest()` | `ov_seven_at_rest` (runtime/smo_ov_input.c) |
| `nn::hid::MergeSingleJoyAsDualJoy(unsigned int const&, unsigned int const&)` | `ov_result_ok` (runtime/smo_ov_input.c) |
| `nn::hid::ResetSevenSixAxisSensorTimestamp()` | `ov_result_ok` (runtime/smo_ov_input.c) |
| `nn::hid::SetNpadJoyAssignmentModeDual(unsigned int const&)` | `ov_nothing` (runtime/smo_ov_input.c) |
| `nn::hid::SetNpadJoyHoldType(nn::hid::NpadJoyHoldType)` | `ov_hold_type` (runtime/ov_input.c) |
| `nn::hid::SetSupportedNpadIdType(unsigned int const*, unsigned long)` | `ov_supported_ids` (runtime/ov_input.c) |
| `nn::hid::SetSupportedNpadStyleSet(nn::util::BitFlagSet<32, nn::hid::NpadStyleTag>)` | `ov_supported_styles` (runtime/ov_input.c) |
| `nn::hid::ShowControllerSupport(nn::hid::ControllerSupportResultInfo*, nn::hid::ControllerSupportArg const&)` | `ov_controller_support` (runtime/ov_input.c) |
| `nn::hid::StartSevenSixAxisSensor()` | `ov_result_ok` (runtime/smo_ov_input.c) |
| `nn::hid::StopSevenSixAxisSensor()` | `ov_result_ok` (runtime/smo_ov_input.c) |
| `nn::nfp::AttachActivateEvent(nn::os::SystemEventType*, nn::nfp::DeviceHandle const&)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nfp::AttachDeactivateEvent(nn::os::SystemEventType*, nn::nfp::DeviceHandle const&)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nfp::Finalize()` | `ov_nfp_finalize` (runtime/ov_system.c) |
| `nn::nfp::GetDeviceState(nn::nfp::DeviceHandle const&)` | `ov_nfp_device_state` (runtime/ov_system.c) |
| `nn::nfp::GetModelInfo(nn::nfp::ModelInfo*, nn::nfp::DeviceHandle const&)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nfp::GetNpadId(unsigned int*, nn::nfp::DeviceHandle const&)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nfp::GetTagInfo(nn::nfp::TagInfo*, nn::nfp::DeviceHandle const&)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nfp::Initialize()` | `ov_nfp_initialize` (runtime/ov_system.c) |
| `nn::nfp::ListDevices(nn::nfp::DeviceHandle*, int*, int)` | `ov_nfp_list` (runtime/ov_system.c) |
| `nn::nfp::Mount(nn::nfp::DeviceHandle const&, nn::nfp::ModelType, nn::nfp::MountTarget)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nfp::StartDetection(nn::nfp::DeviceHandle const&)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nfp::StopDetection(nn::nfp::DeviceHandle const&)` | `ov_nfp_no_device` (runtime/ov_system.c) |
| `nn::nifm::GetCurrentPrimaryIpAddress(in_addr*)` | `ov_nifm_address` (runtime/smo_ov_network.c) |
| `nn::nifm::GetCurrentProxySetting(nn::nifm::ProxySetting*)` | `ov_nifm_address` (runtime/smo_ov_network.c) |
| `nn::nifm::HandleNetworkRequestResult()` | `ov_nifm_handle` (runtime/smo_ov_network.c) |
| `nn::nifm::Initialize()` | `ov_nifm_initialize` (runtime/smo_ov_network.c) |
| `nn::nifm::IsNetworkAvailable()` | `ov_false` (runtime/smo_ov_network.c) |
| `nn::nifm::IsNetworkRequestOnHold()` | `ov_false` (runtime/smo_ov_network.c) |
| `nn::nifm::SubmitNetworkRequest()` | `ov_nifm_submit` (runtime/smo_ov_network.c) |
| `nn::nifm::SubmitNetworkRequestAndWait()` | `ov_nifm_submit` (runtime/smo_ov_network.c) |
| `nn::oe::FinishStartupLogo()` | `ov_finish_logo` (runtime/ov_system.c) |
| `nn::oe::GetCurrentFocusState()` | `ov_focus_state` (runtime/ov_system.c) |
| `nn::oe::GetDesiredLanguage()` | `ov_desired_language` (runtime/ov_system.c) |
| `nn::oe::GetExpectedVolumeBalance(float*, float*)` | `ov_get_balance` (runtime/ov_system.c) |
| `nn::oe::GetOperationMode()` | `ov_operation_mode` (runtime/ov_system.c) |
| `nn::oe::GetPerformanceMode()` | `ov_performance_mode` (runtime/ov_system.c) |
| `nn::oe::Initialize()` | `ov_oe_initialize` (runtime/ov_system.c) |
| `nn::oe::SetCpuBoostMode(nn::oe::CpuBoostMode)` | `ov_cpu_boost` (runtime/ov_system.c) |
| `nn::oe::SetExpectedVolumeBalance(float, float)` | `ov_set_balance` (runtime/ov_system.c) |
| `nn::oe::SetFocusHandlingMode(nn::oe::FocusHandlingMode)` | `ov_focus_mode` (runtime/ov_system.c) |
| `nn::oe::SetOperationModeChangedNotificationEnabled(bool)` | `ov_operation_enabled` (runtime/ov_system.c) |
| `nn::oe::SetPerformanceConfiguration(nn::oe::PerformanceMode, int)` | `ov_performance_config` (runtime/ov_system.c) |
| `nn::oe::SetPerformanceModeChangedNotificationEnabled(bool)` | `ov_performance_enabled` (runtime/ov_system.c) |
| `nn::oe::SetResumeNotificationEnabled(bool)` | `ov_resume_enabled` (runtime/ov_system.c) |
| `nn::oe::SetUserInactivityDetectionTimeExtended(bool)` | `ov_inactivity_extended` (runtime/ov_system.c) |
| `nn::oe::TryPopNotificationMessage(unsigned int*)` | `ov_try_pop` (runtime/ov_system.c) |
| `nn::pctl::ConfirmStereoVisionRestrictionConfigurable()` | `ov_ok` (runtime/smo_ov_network.c) |
| `nn::pctl::GetStereoVisionRestriction()` | `ov_false` (runtime/smo_ov_network.c) |
| `nn::pctl::RequestStereoVisionRestrictionConfigurationPermission()` | `ov_ok` (runtime/smo_ov_network.c) |
| `nn::pctl::SetStereoVisionRestriction(bool)` | `ov_nothing` (runtime/smo_ov_network.c) |
| `nn::pl::GetSharedFontAddress(nn::pl::SharedFontType)` | `ov_font_address` (runtime/ov_system.c) |
| `nn::pl::GetSharedFontLoadState(nn::pl::SharedFontType)` | `ov_font_state` (runtime/ov_system.c) |
| `nn::pl::GetSharedFontSize(nn::pl::SharedFontType)` | `ov_font_size` (runtime/ov_system.c) |
| `nn::prepo::PlayReport::Add(char const*, double)` | `ov_ok` (runtime/smo_ov_network.c) |
| `nn::prepo::PlayReport::Add(char const*, long)` | `ov_ok` (runtime/smo_ov_network.c) |
| `nn::prepo::PlayReport::Add(char const*, nn::prepo::Any64BitId const&)` | `ov_ok` (runtime/smo_ov_network.c) |
| `nn::prepo::PlayReport::PlayReport(char const*)` | `ov_nothing` (runtime/smo_ov_network.c) |
| `nn::prepo::PlayReport::Save(nn::account::Uid const&)` | `ov_report_save` (runtime/ov_system.c) |
| `nn::prepo::PlayReport::SetBuffer(void*, unsigned long)` | `ov_ok` (runtime/smo_ov_network.c) |
| `nn::settings::operator==(nn::settings::LanguageCode const&, nn::settings::Language const&)` | `ov_language_code_equal` (runtime/smo_ov_system.c) |
| `nn::socket::Initialize(void*, unsigned long, unsigned long, int)` | `ov_socket_initialize` (runtime/smo_ov_network.c) |
| `nn::swkbd::ShowKeyboard(nn::swkbd::String*, nn::swkbd::ShowKeyboardArg const&)` | `ov_show_keyboard` (runtime/swkbd.c) |
| `nn::time::Finalize()` | `ov_time_finalize` (runtime/ov_system.c) |
| `nn::time::Initialize()` | `ov_time_initialize` (runtime/ov_system.c) |
| `nn::time::IsInitialized()` | `ov_time_ready` (runtime/ov_system.c) |
| `nn::time::StandardUserSystemClock::GetCurrentTime(nn::time::PosixTime*)` | `ov_current_time` (runtime/ov_system.c) |
| `nn::time::ToCalendarTime(nn::time::CalendarTime*, nn::time::CalendarAdditionalInfo*, nn::time::PosixTime const&)` | `ov_to_calendar` (runtime/ov_system.c) |
| `nn::time::ToPosixTimeFromUtc(nn::time::CalendarTime const&)` | `ov_to_posix_utc` (runtime/ov_system.c) |
| `nn::vi::CreateLayer(nn::vi::Layer**, nn::vi::Display*)` | `ov_create_layer` (runtime/ov_gfx.c) |
| `nn::vi::GetDisplayVsyncEvent(nn::os::SystemEventType*, nn::vi::Display*)` | `ov_vsync_event` (runtime/ov_gfx.c) |
| `nn::vi::GetNativeWindow(void**, nn::vi::Layer*)` | `ov_native_window` (runtime/ov_gfx.c) |
| `nn::vi::Initialize()` | `ov_vi_initialize` (runtime/ov_gfx.c) |
| `nn::vi::OpenDefaultDisplay(nn::vi::Display**)` | `ov_open_display` (runtime/ov_gfx.c) |
| `nnsslInitialize` | `ov_ssl_initialize` (runtime/smo_ov_network.c) |
| `void nn::hid::GetTouchScreenState<1ul>(nn::hid::TouchScreenState<1ul>*)` | `ov_touch_state` (runtime/smo_ov_input.c) |

## Assinatura difere

| Símbolo | Override |
|---|---|

## Falta (importados por main/subsdk0, sem override)

- `nn::account::AsyncContext::AsyncContext()`
- `nn::account::AsyncContext::Cancel()`
- `nn::account::AsyncContext::GetResult()`
- `nn::account::AsyncContext::GetSystemEvent(nn::os::SystemEvent*)`
- `nn::account::AsyncContext::HasDone(bool*)`
- `nn::account::AsyncContext::~AsyncContext()`
- `nn::account::EnsureNetworkServiceAccountAvailable(nn::account::UserHandle const&)`
- `nn::account::EnsureNetworkServiceAccountIdTokenCacheAsync(nn::account::AsyncContext*, nn::account::UserHandle const&)`
- `nn::account::GetNetworkServiceAccountId(nn::account::NetworkServiceAccountId*, nn::account::UserHandle const&)`
- `nn::account::LoadNetworkServiceAccountIdTokenCache(unsigned long*, char*, unsigned long, nn::account::UserHandle const&)`
- `nn::audio::AcquireAudioDeviceSwitchNotification(nn::os::SystemEvent*)`
- `nn::audio::AcquireFinalMix(nn::audio::AudioRendererConfig*, nn::audio::FinalMixType*, int)`
- `nn::audio::AcquireMemoryPool(nn::audio::AudioRendererConfig*, nn::audio::MemoryPoolType*, void*, unsigned long)`
- `nn::audio::AcquireSubMix(nn::audio::AudioRendererConfig*, nn::audio::SubMixType*, int, int)`
- `nn::audio::AcquireVoiceSlot(nn::audio::AudioRendererConfig*, nn::audio::VoiceType*, int, int, nn::audio::SampleFormat, int, void const*, unsigned long)`
- `nn::audio::AddAux(nn::audio::AudioRendererConfig*, nn::audio::AuxType*, nn::audio::FinalMixType*, void*, void*, unsigned long)`
- `nn::audio::AddAux(nn::audio::AudioRendererConfig*, nn::audio::AuxType*, nn::audio::SubMixType*, void*, void*, unsigned long)`
- `nn::audio::AddCircularBufferSink(nn::audio::AudioRendererConfig*, nn::audio::CircularBufferSinkType*, nn::audio::FinalMixType*, signed char const*, int, void*, unsigned long, nn::audio::SampleFormat)`
- `nn::audio::AddDelay(nn::audio::AudioRendererConfig*, nn::audio::DelayType*, void*, unsigned long, nn::audio::FinalMixType*, nn::TimeSpan, int)`
- `nn::audio::AddDelay(nn::audio::AudioRendererConfig*, nn::audio::DelayType*, void*, unsigned long, nn::audio::SubMixType*, nn::TimeSpan, int)`
- `nn::audio::AddDeviceSink(nn::audio::AudioRendererConfig*, nn::audio::DeviceSinkType*, nn::audio::FinalMixType*, signed char const*, int, char const*)`
- `nn::audio::AppendAudioOutBuffer(nn::audio::AudioOut*, nn::audio::AudioOutBuffer*)`
- `nn::audio::AppendWaveBuffer(nn::audio::VoiceType*, nn::audio::WaveBuffer const*)`
- `nn::audio::CalculatePolyphaseResamplerActualOutputSampleRate(int, int)`
- `nn::audio::CloseAudioOut(nn::audio::AudioOut*)`
- `nn::audio::CloseAudioRenderer(nn::audio::AudioRendererHandle)`
- `nn::audio::ExecuteAudioRendererRendering(nn::audio::AudioRendererHandle)`
- `nn::audio::GetActiveAudioDeviceName(nn::audio::AudioDeviceName*)`
- `nn::audio::GetActiveChannelCount()`
- `nn::audio::GetAudioOutBufferDataPointer(nn::audio::AudioOutBuffer const*)`
- `nn::audio::GetAudioOutBufferDataSize(nn::audio::AudioOutBuffer const*)`
- `nn::audio::GetAudioOutChannelCount(nn::audio::AudioOut const*)`
- `nn::audio::GetAudioOutPlayedSampleCount(nn::audio::AudioOut const*)`
- `nn::audio::GetAudioOutSampleFormat(nn::audio::AudioOut const*)`
- `nn::audio::GetAudioOutSampleRate(nn::audio::AudioOut const*)`
- `nn::audio::GetAudioRendererConfigWorkBufferSize(nn::audio::AudioRendererParameter const&)`
- `nn::audio::GetAudioRendererWorkBufferSize(nn::audio::AudioRendererParameter const&)`
- `nn::audio::GetAuxSampleCount(nn::audio::AuxType const*)`
- `nn::audio::GetAuxSampleRate(nn::audio::AuxType const*)`
- `nn::audio::GetMemoryPoolState(nn::audio::MemoryPoolType const*)`
- `nn::audio::GetReleasedAudioOutBuffer(nn::audio::AudioOut*)`
- `nn::audio::GetReleasedWaveBuffer(nn::audio::VoiceType*)`
- `nn::audio::GetRequiredBufferSizeForAuxSendReturnBuffer(nn::audio::AudioRendererParameter const*, int, int)`
- `nn::audio::GetRequiredBufferSizeForCircularBufferSink(nn::audio::AudioRendererParameter const*, int, int, nn::audio::SampleFormat)`
- `nn::audio::GetRequiredBufferSizeForDelay(nn::TimeSpan, int, int)`
- `nn::audio::GetRequiredBufferSizeForPerformanceFrames(nn::audio::AudioRendererParameter const&)`
- `nn::audio::GetRequiredBufferSizeForPolyphaseResampler(int, int, int, bool)`
- `nn::audio::GetSampleByteSize(nn::audio::SampleFormat)`
- `nn::audio::GetSinkNodeId(nn::audio::CircularBufferSinkType const*)`
- `nn::audio::GetSinkNodeId(nn::audio::DeviceSinkType const*)`
- `nn::audio::GetSubMixNodeId(nn::audio::SubMixType const*)`
- `nn::audio::GetVoiceNodeId(nn::audio::VoiceType const*)`
- `nn::audio::GetVoicePlayState(nn::audio::VoiceType const*)`
- `nn::audio::GetVoicePlayedSampleCount(nn::audio::VoiceType const*)`
- `nn::audio::InitializeAudioOutParameter(nn::audio::AudioOutParameter*)`
- `nn::audio::InitializeAudioRendererConfig(nn::audio::AudioRendererConfig*, nn::audio::AudioRendererParameter const&, void*, unsigned long)`
- `nn::audio::InitializeAudioRendererParameter(nn::audio::AudioRendererParameter*)`
- `nn::audio::InitializePolyphaseResampler(nn::audio::PolyphaseResamplerType*, void*, unsigned long, int, int, int, bool, float)`
- `nn::audio::IsAuxRemovable(nn::audio::AuxType const*)`
- `nn::audio::IsDelayRemovable(nn::audio::DelayType const*)`
- `nn::audio::IsMemoryPoolAttached(nn::audio::MemoryPoolType const*)`
- `nn::audio::IsValidAudioRendererParameter(nn::audio::AudioRendererParameter const&)`
- `nn::audio::IsVoiceDroppedFlagOn(nn::audio::VoiceType const*)`
- `nn::audio::IsVoiceValid(nn::audio::VoiceType const*)`
- `nn::audio::ListAudioDeviceName(nn::audio::AudioDeviceName*, int)`
- `nn::audio::OpenAudioRenderer(nn::audio::AudioRendererHandle*, nn::os::SystemEvent*, nn::audio::AudioRendererParameter const&, void*, unsigned long)`
- `nn::audio::OpenDefaultAudioOut(nn::audio::AudioOut*, nn::audio::AudioOutParameter const&)`
- `nn::audio::PerformanceInfo::MoveToNextFrame()`
- `nn::audio::PerformanceInfo::PerformanceInfo()`
- `nn::audio::PerformanceInfo::SetBuffer(void const*, unsigned long)`
- `nn::audio::PerformanceInfo::~PerformanceInfo()`
- `nn::audio::ProcessPolyphaseResamplerBuffer(nn::audio::PolyphaseResamplerType*, int*, short*, unsigned long, short const*, int)`
- `nn::audio::ReadAuxSendBuffer(nn::audio::AuxType*, int*, int)`
- `nn::audio::ReadCircularBufferSink(nn::audio::CircularBufferSinkType*, void*, unsigned long)`
- `nn::audio::ReleaseMemoryPool(nn::audio::AudioRendererConfig*, nn::audio::MemoryPoolType*)`
- `nn::audio::ReleaseVoiceSlot(nn::audio::AudioRendererConfig*, nn::audio::VoiceType*)`
- `nn::audio::RemoveAux(nn::audio::AudioRendererConfig*, nn::audio::AuxType*, nn::audio::FinalMixType*)`
- `nn::audio::RemoveAux(nn::audio::AudioRendererConfig*, nn::audio::AuxType*, nn::audio::SubMixType*)`
- `nn::audio::RemoveDelay(nn::audio::AudioRendererConfig*, nn::audio::DelayType*, nn::audio::FinalMixType*)`
- `nn::audio::RemoveDelay(nn::audio::AudioRendererConfig*, nn::audio::DelayType*, nn::audio::SubMixType*)`
- `nn::audio::RequestAttachMemoryPool(nn::audio::MemoryPoolType*)`
- `nn::audio::RequestDetachMemoryPool(nn::audio::MemoryPoolType*)`
- `nn::audio::RequestUpdateAudioRenderer(nn::audio::AudioRendererHandle, nn::audio::AudioRendererConfig const*)`
- `nn::audio::SetAudioDeviceOutputVolume(nn::audio::AudioDeviceName const*, float)`
- `nn::audio::SetAudioOutBufferInfo(nn::audio::AudioOutBuffer*, void*, unsigned long, unsigned long)`
- `nn::audio::SetAuxEnabled(nn::audio::AuxType*, bool)`
- `nn::audio::SetAuxInputOutput(nn::audio::AuxType*, signed char const*, signed char const*, int)`
- `nn::audio::SetDelayChannelSpread(nn::audio::DelayType*, float)`
- `nn::audio::SetDelayDryGain(nn::audio::DelayType*, float)`
- `nn::audio::SetDelayEnabled(nn::audio::DelayType*, bool)`
- `nn::audio::SetDelayFeedbackGain(nn::audio::DelayType*, float)`
- `nn::audio::SetDelayInGain(nn::audio::DelayType*, float)`
- `nn::audio::SetDelayInputOutput(nn::audio::DelayType*, signed char const*, signed char const*, int)`
- `nn::audio::SetDelayLowPassAmount(nn::audio::DelayType*, float)`
- `nn::audio::SetDelayTime(nn::audio::DelayType*, nn::TimeSpan)`
- `nn::audio::SetDownMixParameter(nn::audio::DeviceSinkType*, nn::audio::DeviceSinkType::DownMixParameter const*)`
- `nn::audio::SetDownMixParameterEnabled(nn::audio::DeviceSinkType*, bool)`
- `nn::audio::SetPerformanceFrameBuffer(nn::audio::AudioRendererConfig*, void*, unsigned long)`
- `nn::audio::SetSubMixDestination(nn::audio::AudioRendererConfig*, nn::audio::SubMixType*, nn::audio::FinalMixType*)`
- `nn::audio::SetSubMixDestination(nn::audio::AudioRendererConfig*, nn::audio::SubMixType*, nn::audio::SubMixType*)`
- `nn::audio::SetSubMixMixVolume(nn::audio::SubMixType*, nn::audio::FinalMixType*, float, int, int)`
- `nn::audio::SetSubMixMixVolume(nn::audio::SubMixType*, nn::audio::SubMixType*, float, int, int)`
- `nn::audio::SetVoiceBiquadFilterParameter(nn::audio::VoiceType*, int, nn::audio::BiquadFilterParameter const&)`
- `nn::audio::SetVoiceDestination(nn::audio::AudioRendererConfig*, nn::audio::VoiceType*, nn::audio::FinalMixType*)`
- `nn::audio::SetVoiceDestination(nn::audio::AudioRendererConfig*, nn::audio::VoiceType*, nn::audio::SubMixType*)`
- `nn::audio::SetVoiceMixVolume(nn::audio::VoiceType*, nn::audio::FinalMixType*, float, int, int)`
- `nn::audio::SetVoiceMixVolume(nn::audio::VoiceType*, nn::audio::SubMixType*, float, int, int)`
- `nn::audio::SetVoicePitch(nn::audio::VoiceType*, float)`
- `nn::audio::SetVoicePlayState(nn::audio::VoiceType*, nn::audio::VoiceType::PlayState)`
- `nn::audio::SetVoicePriority(nn::audio::VoiceType*, int)`
- `nn::audio::SetVoiceVolume(nn::audio::VoiceType*, float)`
- `nn::audio::StartAudioOut(nn::audio::AudioOut*)`
- `nn::audio::StartAudioRenderer(nn::audio::AudioRendererHandle)`
- `nn::audio::StopAudioOut(nn::audio::AudioOut*)`
- `nn::audio::StopAudioRenderer(nn::audio::AudioRendererHandle)`
- `nn::audio::WriteAuxReturnBuffer(nn::audio::AuxType*, int const*, int)`
- `nn::bcat::DeliveryCacheDirectory::DeliveryCacheDirectory()`
- `nn::bcat::DeliveryCacheDirectory::Open(nn::bcat::DirectoryName const&)`
- `nn::bcat::DeliveryCacheDirectory::Read(int*, nn::bcat::DeliveryCacheDirectoryEntry*, int)`
- `nn::bcat::DeliveryCacheDirectory::~DeliveryCacheDirectory()`
- `nn::bcat::DeliveryCacheFile::Close()`
- `nn::bcat::DeliveryCacheFile::DeliveryCacheFile()`
- `nn::bcat::DeliveryCacheFile::Open(char const*)`
- `nn::bcat::DeliveryCacheFile::Read(unsigned long*, long, void*, unsigned long)`
- `nn::bcat::DeliveryCacheFile::~DeliveryCacheFile()`
- `nn::bcat::DeliveryCacheProgress::DeliveryCacheProgress()`
- `nn::bcat::DeliveryCacheProgress::Update()`
- `nn::bcat::DeliveryCacheProgress::~DeliveryCacheProgress()`
- `nn::bcat::EnumerateDeliveryCacheDirectory(int*, nn::bcat::DirectoryName*, int)`
- `nn::crypto::GenerateSha1Hash(void*, unsigned long, void const*, unsigned long)`
- `nn::crypto::detail::Md5Impl::GetHash(void*, unsigned long)`
- `nn::crypto::detail::Md5Impl::Initialize()`
- `nn::crypto::detail::Md5Impl::Update(void const*, unsigned long)`
- `nn::crypto::detail::Md5Impl::~Md5Impl()`
- `nn::detail::UnexpectedDefaultImpl(char const*, char const*, int)`
- `nn::diag::GetAllModuleInfo(nn::diag::ModuleInfo**, void*, unsigned long)`
- `nn::diag::GetBacktrace(unsigned long*, int)`
- `nn::diag::GetRequiredBufferSizeForGetAllModuleInfo()`
- `nn::diag::GetSymbolName(char*, unsigned long, unsigned long)`
- `nn::diag::GetSymbolSize(unsigned long)`
- `nn::diag::InitializeAbortObserverHolder(nn::diag::AbortObserverHolder*, void (*)(nn::diag::AbortInfo const&))`
- `nn::diag::IsDebuggerAttached()`
- `nn::diag::RegisterAbortObserver(nn::diag::AbortObserverHolder*)`
- `nn::diag::detail::AbortImpl(char const*, char const*, char const*, int)`
- `nn::diag::detail::AbortImpl(char const*, char const*, char const*, int, nn::Result const*, char const*, ...)`
- `nn::diag::detail::LogImpl(nn::diag::LogMetaData const&, char const*, ...)`
- `nn::diag::detail::NotNullImpl(unsigned long)`
- `nn::diag::detail::OnAssertionFailure(nn::diag::AssertionType, char const*, char const*, char const*, int)`
- `nn::diag::detail::PutImpl(nn::diag::LogMetaData const&, char const*, unsigned long)`
- `nn::err::ReportMultimediaError(nn::Result, movie::MultimediaTelemetryReport const&)`
- `nn::fontll::ScalableFontEngine::AcquireGlyphmap(unsigned int, unsigned short)`
- `nn::fontll::ScalableFontEngine::AcquireOtfKerning(nn::fontll::OtfKerningTable const*, unsigned int, unsigned int, unsigned int)`
- `nn::fontll::ScalableFontEngine::AcquireOtfKerningFirst(nn::fontll::OtfKerningTable const*, unsigned int, unsigned int)`
- `nn::fontll::ScalableFontEngine::AcquireOtfKerningLast(nn::fontll::OtfKerningTable const*, unsigned int, unsigned int)`
- `nn::fontll::ScalableFontEngine::CheckGlyphExist(unsigned int)`
- `nn::fontll::ScalableFontEngine::Finalize()`
- `nn::fontll::ScalableFontEngine::FinalizeOtfKerningTable(nn::fontll::OtfKerningTable*, void (*)(void*, void*), void*)`
- `nn::fontll::ScalableFontEngine::GetAdvance(short*, short*, int*, int*, unsigned int, unsigned short)`
- `nn::fontll::ScalableFontEngine::GetError()`
- `nn::fontll::ScalableFontEngine::GetFontMetrics(nn::fontll::Metrics*)`
- `nn::fontll::ScalableFontEngine::GetKerning(int*, int*, unsigned int, unsigned int)`
- `nn::fontll::ScalableFontEngine::GetPointerToWorkBuffer()`
- `nn::fontll::ScalableFontEngine::Initialize(void*, unsigned int)`
- `nn::fontll::ScalableFontEngine::InitializeOtfKerningTable(void* (*)(unsigned long, unsigned long, void*), void*, bool)`
- `nn::fontll::ScalableFontEngine::LoadFont(char*, void const*, unsigned int, unsigned int)`
- `nn::fontll::ScalableFontEngine::ReleasesGlyph(void*)`
- `nn::fontll::ScalableFontEngine::ScalableFontEngine()`
- `nn::fontll::ScalableFontEngine::SetAutoHint(bool)`
- `nn::fontll::ScalableFontEngine::SetBoldWeight(int)`
- `nn::fontll::ScalableFontEngine::SetFlags(nn::fontll::ScalableFontEngine::Flags)`
- `nn::fontll::ScalableFontEngine::SetFont(char*)`
- `nn::fontll::ScalableFontEngine::SetOutlineWidth(unsigned short)`
- `nn::fontll::ScalableFontEngine::SetScale(int, int, int, int)`
- `nn::fontll::ScalableFontEngineHelper::Decode(void const*, unsigned int)`
- `nn::friends::AsyncContext::AsyncContext()`
- `nn::friends::AsyncContext::GetSystemEvent(nn::os::SystemEvent*)`
- `nn::friends::AsyncContext::~AsyncContext()`
- `nn::friends::GetProfileList(nn::friends::AsyncContext*, nn::friends::Profile*, nn::account::NetworkServiceAccountId const*, int)`
- `nn::friends::Profile::Profile()`
- `nn::hid::GetSixAxisSensorHandles(nn::hid::SixAxisSensorHandle*, int, unsigned int const&, nn::util::BitFlagSet<32, nn::hid::NpadStyleTag>)`
- `nn::hid::GetSixAxisSensorStates(nn::hid::SixAxisSensorState*, int, nn::hid::SixAxisSensorHandle const&)`
- `nn::hid::GetVibrationDeviceHandles(nn::hid::VibrationDeviceHandle*, int, unsigned int const&, nn::util::BitFlagSet<32, nn::hid::NpadStyleTag>)`
- `nn::hid::InitializeVibrationDevice(nn::hid::VibrationDeviceHandle const&)`
- `nn::hid::IsVibrationDeviceMounted(nn::hid::VibrationDeviceHandle const&)`
- `nn::hid::SendVibrationValue(nn::hid::VibrationDeviceHandle const&, nn::hid::VibrationValue const&)`
- `nn::hid::StartSixAxisSensor(nn::hid::SixAxisSensorHandle const&)`
- `nn::hid::VibrationMixer::SetMixMode(nn::hid::VibrationMixMode)`
- `nn::hid::VibrationMixer::VibrationMixer()`
- `nn::hid::VibrationNode::SetModulationTo(nn::hid::VibrationNode const*, nn::hid::VibrationModulation const&)`
- `nn::hid::VibrationNode::Update()`
- `nn::hid::VibrationNodeConnection::Connect(nn::hid::VibrationNode*, nn::hid::VibrationNode*)`
- `nn::hid::VibrationNodeConnection::Disconnect()`
- `nn::hid::VibrationNodeConnection::VibrationNodeConnection()`
- `nn::hid::VibrationNodeConnection::VibrationNodeConnection(nn::hid::VibrationNode*, nn::hid::VibrationNode*)`
- `nn::hid::VibrationPlayer::Load(void const*, unsigned long)`
- `nn::hid::VibrationPlayer::Play()`
- `nn::hid::VibrationPlayer::SetCurrentPosition(int)`
- `nn::hid::VibrationPlayer::SetLoop(bool)`
- `nn::hid::VibrationPlayer::Stop()`
- `nn::hid::VibrationPlayer::VibrationPlayer()`
- `nn::hid::VibrationTarget::SetVibrationDeviceHandle(nn::hid::VibrationDeviceHandle const&)`
- `nn::hid::VibrationTarget::UnsetVibrationDeviceHandle()`
- `nn::hid::VibrationTarget::VibrationTarget()`
- `nn::hid::VibrationWriter::VibrationWriter()`
- `nn::hid::VibrationWriter::Write(nn::hid::VibrationValue const&)`
- `nn::image::JpegDecoder::Analyze()`
- `nn::image::JpegDecoder::Decode(void*, unsigned long, int, void*, unsigned long)`
- `nn::image::JpegDecoder::JpegDecoder()`
- `nn::image::JpegDecoder::SetImageData(void const*, unsigned long)`
- `nn::image::JpegDecoder::~JpegDecoder()`
- `nn::lmem::AllocateFromExpHeap(nn::lmem::detail::HeapHead*, unsigned long)`
- `nn::lmem::AllocateFromFrameHeap(nn::lmem::detail::HeapHead*, unsigned long, int)`
- `nn::lmem::CreateExpHeap(void*, unsigned long, int)`
- `nn::lmem::CreateFrameHeap(void*, unsigned long, int)`
- `nn::lmem::DestroyFrameHeap(nn::lmem::detail::HeapHead*)`
- `nn::lmem::FreeToExpHeap(nn::lmem::detail::HeapHead*, void*)`
- `nn::mem::StandardAllocator::Allocate(unsigned long)`
- `nn::mem::StandardAllocator::Allocate(unsigned long, unsigned long)`
- `nn::mem::StandardAllocator::Finalize()`
- `nn::mem::StandardAllocator::Free(void*)`
- `nn::mem::StandardAllocator::Initialize(void*, unsigned long)`
- `nn::mem::StandardAllocator::Initialize(void*, unsigned long, bool)`
- `nn::mem::StandardAllocator::Reallocate(void*, unsigned long)`
- `nn::mem::StandardAllocator::StandardAllocator()`
- `nn::mem::StandardAllocator::StandardAllocator(void*, unsigned long)`
- `nn::nfp::Unmount(nn::nfp::DeviceHandle const&)`
- `nn::nsd::ResolveEx(nn::nsd::Fqdn*, nn::nsd::Fqdn const&)`
- `nn::oe::BeginBlockingHomeButton()`
- `nn::oe::DisableRecording()`
- `nn::oe::EnableRecording()`
- `nn::oe::EndBlockingHomeButton()`
- `nn::oe::GetPerformanceConfiguration(nn::oe::PerformanceMode)`
- `nn::oe::IsUserInactivityDetectionTimeExtended()`
- `nn::oe::SetScreenShotImageOrientation(nn::album::ImageOrientation)`
- `nn::os::AllocateMemoryBlock(unsigned long*, unsigned long)`
- `nn::os::AllocateTlsSlot(nn::os::TlsSlot*, void (*)(unsigned long))`
- `nn::os::AttachReadableHandleToSystemEvent(nn::os::SystemEventType*, unsigned int, bool, nn::os::EventClearMode)`
- `nn::os::BroadcastConditionVariable(nn::os::ConditionVariableType*)`
- `nn::os::ChangeThreadPriority(nn::os::ThreadType*, int)`
- `nn::os::ClearEvent(nn::os::EventType*)`
- `nn::os::ClearLightEvent(nn::os::LightEventType*)`
- `nn::os::ConvertToTick(nn::TimeSpan)`
- `nn::os::ConvertToTimeSpan(nn::os::Tick)`
- `nn::os::CreateThread(nn::os::ThreadType*, void (*)(void*), void*, void*, unsigned long, int)`
- `nn::os::CreateThread(nn::os::ThreadType*, void (*)(void*), void*, void*, unsigned long, int, int)`
- `nn::os::DestroySystemEvent(nn::os::SystemEventType*)`
- `nn::os::DestroyThread(nn::os::ThreadType*)`
- `nn::os::FinalizeConditionVariable(nn::os::ConditionVariableType*)`
- `nn::os::FinalizeEvent(nn::os::EventType*)`
- `nn::os::FinalizeLightEvent(nn::os::LightEventType*)`
- `nn::os::FinalizeMessageQueue(nn::os::MessageQueueType*)`
- `nn::os::FinalizeMutex(nn::os::MutexType*)`
- `nn::os::FreeTlsSlot(nn::os::TlsSlot)`
- `nn::os::GenerateRandomBytes(void*, unsigned long)`
- `nn::os::GetCurrentCoreNumber()`
- `nn::os::GetCurrentFiber()`
- `nn::os::GetCurrentStackInfo(unsigned long*, unsigned long*)`
- `nn::os::GetCurrentThread()`
- `nn::os::GetHostArgc()`
- `nn::os::GetHostArgv()`
- `nn::os::GetSystemTick()`
- `nn::os::GetSystemTickFrequency()`
- `nn::os::GetThreadAvailableCoreMask()`
- `nn::os::GetThreadId(nn::os::ThreadType const*)`
- `nn::os::GetThreadNamePointer(nn::os::ThreadType const*)`
- `nn::os::GetThreadPriority(nn::os::ThreadType const*)`
- `nn::os::GetTlsValue(nn::os::TlsSlot)`
- `nn::os::InitializeConditionVariable(nn::os::ConditionVariableType*)`
- `nn::os::InitializeEvent(nn::os::EventType*, bool, nn::os::EventClearMode)`
- `nn::os::InitializeLightEvent(nn::os::LightEventType*, bool, nn::os::EventClearMode)`
- `nn::os::InitializeMessageQueue(nn::os::MessageQueueType*, unsigned long*, unsigned long)`
- `nn::os::InitializeMutex(nn::os::MutexType*, bool, int)`
- `nn::os::JamMessageQueue(nn::os::MessageQueueType*, unsigned long)`
- `nn::os::LockMutex(nn::os::MutexType*)`
- `nn::os::ReceiveMessageQueue(unsigned long*, nn::os::MessageQueueType*)`
- `nn::os::SendMessageQueue(nn::os::MessageQueueType*, unsigned long)`
- `nn::os::SetMemoryHeapSize(unsigned long)`
- `nn::os::SetThreadCoreMask(nn::os::ThreadType*, int, unsigned long)`
- `nn::os::SetThreadName(nn::os::ThreadType*, char const*)`
- `nn::os::SetThreadNamePointer(nn::os::ThreadType*, char const*)`
- `nn::os::SetTlsValue(nn::os::TlsSlot, unsigned long)`
- `nn::os::SetUserExceptionHandler(void (*)(nn::os::UserExceptionInfo*), void*, unsigned long, nn::os::UserExceptionInfo*)`
- `nn::os::SignalConditionVariable(nn::os::ConditionVariableType*)`
- `nn::os::SignalEvent(nn::os::EventType*)`
- `nn::os::SignalLightEvent(nn::os::LightEventType*)`
- `nn::os::SleepThread(nn::TimeSpan)`
- `nn::os::StartThread(nn::os::ThreadType*)`
- `nn::os::TimedWaitConditionVariable(nn::os::ConditionVariableType*, nn::os::MutexType*, nn::TimeSpan)`
- `nn::os::TimedWaitLightEvent(nn::os::LightEventType*, nn::TimeSpan)`
- `nn::os::TimedWaitSystemEvent(nn::os::SystemEventType*, nn::TimeSpan)`
- `nn::os::TryJamMessageQueue(nn::os::MessageQueueType*, unsigned long)`
- `nn::os::TryLockMutex(nn::os::MutexType*)`
- `nn::os::TryReceiveMessageQueue(unsigned long*, nn::os::MessageQueueType*)`
- `nn::os::TrySendMessageQueue(nn::os::MessageQueueType*, unsigned long)`
- `nn::os::TryWaitEvent(nn::os::EventType*)`
- `nn::os::TryWaitSystemEvent(nn::os::SystemEventType*)`
- `nn::os::UnlockMutex(nn::os::MutexType*)`
- `nn::os::WaitConditionVariable(nn::os::ConditionVariableType*, nn::os::MutexType*)`
- `nn::os::WaitEvent(nn::os::EventType*)`
- `nn::os::WaitLightEvent(nn::os::LightEventType*)`
- `nn::os::WaitSystemEvent(nn::os::SystemEventType*)`
- `nn::os::WaitThread(nn::os::ThreadType*)`
- `nn::os::YieldThread()`
- `nn::pl::BeginVrMode()`
- `nn::pl::EndVrMode()`
- `nn::sf::cmif::GetInlineContext()`
- `nn::sf::hipc::CloseClientSessionHandle(nn::svc::Handle)`
- `nn::sf::hipc::ConnectToHipcService(nn::svc::Handle*, char const*)`
- `nn::sf::hipc::FinalizeHipcServiceResolution()`
- `nn::sf::hipc::GetMessageBufferOnTls()`
- `nn::sf::hipc::InitializeHipcServiceResolution()`
- `nn::sf::hipc::SendSyncRequest(nn::svc::Handle, void*, unsigned long)`
- `nn::sf::hipc::detail::HipcMessageBufferAccessor::SetTag(unsigned short)`
- `nn::sf::hipc::detail::HipcMessageBufferAccessor::SetupHeader(void*, unsigned long, nn::sf::hipc::detail::HipcMessageHeaderInfo const&)`
- `nn::sf::impl::detail::ServiceObjectImplBase2::AddReferenceImpl()`
- `nn::sf::impl::detail::ServiceObjectImplBase2::ReleaseImpl()`
- `nn::socket::Accept(int, sockaddr*, unsigned int*)`
- `nn::socket::Bind(int, sockaddr const*, unsigned int)`
- `nn::socket::Close(int)`
- `nn::socket::Connect(int, sockaddr const*, unsigned int)`
- `nn::socket::Fcntl(int, int, ...)`
- `nn::socket::FreeAddrInfo(addrinfo*)`
- `nn::socket::GetAddrInfo(char const*, char const*, addrinfo const*, addrinfo**)`
- `nn::socket::GetLastErrno()`
- `nn::socket::GetSockName(int, sockaddr*, unsigned int*)`
- `nn::socket::GetSockOpt(int, int, int, void*, unsigned int*)`
- `nn::socket::InetHtonl(unsigned int)`
- `nn::socket::InetHtons(unsigned short)`
- `nn::socket::InetNtoa(in_addr)`
- `nn::socket::InetNtohl(unsigned int)`
- `nn::socket::InetNtohs(unsigned short)`
- `nn::socket::InetNtop(int, void const*, char*, unsigned int)`
- `nn::socket::InetPton(int, char const*, void*)`
- `nn::socket::Listen(int, int)`
- `nn::socket::Poll(pollfd*, unsigned long, int)`
- `nn::socket::Recv(int, void*, unsigned long, int)`
- `nn::socket::RecvFrom(int, void*, unsigned long, int, sockaddr*, unsigned int*)`
- `nn::socket::Send(int, void const*, unsigned long, int)`
- `nn::socket::SendTo(int, void const*, unsigned long, int, sockaddr const*, unsigned int)`
- `nn::socket::SetSockOpt(int, int, int, void const*, unsigned int)`
- `nn::socket::Shutdown(int, int)`
- `nn::socket::Socket(int, int, int)`
- `nn::ssl::Context::Create(nn::ssl::Context::SslVersion)`
- `nn::ssl::Context::ImportServerPki(unsigned long*, char const*, unsigned int, nn::ssl::CertificateFormat)`
- `nn::swkbd::GetRequiredStringBufferSize()`
- `nn::swkbd::GetRequiredWorkBufferSize(bool)`
- `nn::swkbd::MakePreset(nn::swkbd::KeyboardConfig*, nn::swkbd::Preset)`
- `nn::swkbd::SetHeaderText(nn::swkbd::KeyboardConfig*, char16_t const*)`
- `nn::swkbd::SetSubText(nn::swkbd::KeyboardConfig*, char16_t const*)`
- `nn::util::BinaryFileHeader::GetFirstBlock()`
- `nn::util::BinaryFileHeader::GetRelocationTable()`
- `nn::util::ConvertCharacterUtf8ToUtf32(unsigned int*, char const*)`
- `nn::util::FloatPi`
- `nn::util::MatrixRowMajor4x3f::ConstantIdentity`
- `nn::util::PickOutCharacterFromUtf8String(char*, char const**)`
- `nn::util::ReferSymbol(void const*)`
- `nn::util::RelocationTable::Relocate()`
- `nn::util::SNPrintf(char*, unsigned long, char const*, ...)`
- `nn::util::VSNPrintf(char*, unsigned long, char const*, std::__va_list)`
- `nn::util::detail::AngleIndexHalfRound`
- `nn::util::detail::AtanCoefficients`
- `nn::util::detail::CosCoefficients`
- `nn::util::detail::Float1Divided2Pi`
- `nn::util::detail::Float2Pi`
- `nn::util::detail::FloatDegree180`
- `nn::util::detail::FloatPi`
- `nn::util::detail::FloatPiDivided2`
- `nn::util::detail::FloatQuaternionEpsilon`
- `nn::util::detail::FloatUlp`
- `nn::util::detail::SinCoefficients`
- `nn::util::detail::SinCosSampleTable`
- `nn::vi::SetLayerScalingMode(nn::vi::Layer*, nn::vi::ScalingMode)`
- `nn::web::OfflineHtmlPageReturnValue::OfflineHtmlPageReturnValue()`
- `nn::web::ShowOfflineHtmlPage(nn::web::OfflineHtmlPageReturnValue*, nn::web::ShowOfflineHtmlPageArg const&)`
- `nn::web::ShowOfflineHtmlPageArg::SetBackgroundKind(nn::web::OfflineBackgroundKind const&)`
- `nn::web::ShowOfflineHtmlPageArg::SetBootDisplayKind(nn::web::OfflineBootDisplayKind)`
- `nn::web::ShowOfflineHtmlPageArg::SetFooterEnabled(bool)`
- `nn::web::ShowOfflineHtmlPageArg::SetPointerEnabled(bool)`
- `nn::web::ShowOfflineHtmlPageArgWithPlayReport::SetPlayReportEnabled(bool)`
- `nn::web::ShowOfflineHtmlPageArgWithPlayReport::ShowOfflineHtmlPageArgWithPlayReport(nn::ApplicationId const&, char const*)`
- `nnMain`
- `nnResultGetDescription`
- `nnResultGetModule`
- `nnResultIsFailure`
- `nnResultIsSuccess`
- `nndetailDiagAbortFormatImpl`
- `nninitStartup`
- `nnosConvertTickToNanoSeconds`
- `nnosCreateThread`
- `nnosDestroyThread`
- `nnosFinalizeEvent`
- `nnosFinalizeMutex`
- `nnosGetCurrentThread`
- `nnosGetDefaultUserExceptionStackForApplication`
- `nnosGetSystemTick`
- `nnosGetSystemTickFrequency`
- `nnosGetThreadCoreMask`
- `nnosGetThreadPriority`
- `nnosInitializeEvent`
- `nnosInitializeMutex`
- `nnosLockMutex`
- `nnosSetThreadCoreMask`
- `nnosSetThreadNamePointer`
- `nnosSignalEvent`
- `nnosSleepThread`
- `nnosStartThread`
- `nnosUnlockMutex`
- `nnosWaitEvent`
- `nnosWaitThread`
- `nnsocketBind`
- `nnsocketClose`
- `nnsocketConnect`
- `nnsocketFcntl`
- `nnsocketGetHostByNameWithOptions`
- `nnsocketGetLastErrno`
- `nnsocketGetPeerName`
- `nnsocketGetSockName`
- `nnsocketGetSockOpt`
- `nnsocketInetHtons`
- `nnsocketInetNtohs`
- `nnsocketPoll`
- `nnsocketRecv`
- `nnsocketResolverGetOption`
- `nnsocketResolverSetOption`
- `nnsocketSend`
- `nnsocketSetLastErrno`
- `nnsocketSetSockOpt`
- `nnsocketSocket`
- `nnsslConnectionCreate`
- `nnsslConnectionDestroy`
- `nnsslConnectionDoHandshakeWithCertBuffer`
- `nnsslConnectionGetConnectionId`
- `nnsslConnectionGetVerifyCertError`
- `nnsslConnectionPending`
- `nnsslConnectionRead`
- `nnsslConnectionSetHostName`
- `nnsslConnectionSetIoMode`
- `nnsslConnectionSetOption`
- `nnsslConnectionSetSessionCacheMode`
- `nnsslConnectionSetSocketDescriptor`
- `nnsslConnectionSetVerifyOption`
- `nnsslConnectionWrite`
- `nnsslContextDestroy`
- `nnsslContextGetContextId`

## Overrides sem referência no SMO

- `nn::codec::GetHardwareOpusDecoderWorkBufferSize(int, int, int)` (runtime/ov_media.c)
- `nn::err::InitializeContextWriterApi()` (runtime/ov_system.c)
- `nn::prepo::AddInternetConnectionStatus(nn::prepo::PlayReport*, char const*, char const*, char const*)` (runtime/ov_system.c)

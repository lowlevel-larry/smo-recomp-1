// Host overrides of the nn::hid functions only Super Mario Odyssey (SDK 7.3.2) imports and whose SDK code talks to
// the hid service directly; the rest of its hid use reaches the nn::hid::detail functions ov_input.c already hosts.
// None of these symbols is in TotK's modules.
#include <stdint.h>
#include <string.h>

#include "host.h"

static void ov_nothing(Cpu *c) { (void)c; }
static void ov_result_ok(Cpu *c) { ret_x(c, 0); }

// The console's own motion sensor ("seven six axis", Labo VR): not present on a PC. States: none.
// int GetSevenSixAxisSensorStates(SevenSixAxisSensorState *out, int count)
static void ov_seven_states(Cpu *c) { ret_x(c, 0); }
// bool IsSevenSixAxisSensorAtRest()
static void ov_seven_at_rest(Cpu *c) { ret_x(c, 1); }
HOST_OVERRIDE("_ZN2nn3hid28InitializeSevenSixAxisSensorEPvm", ov_result_ok);
HOST_OVERRIDE("_ZN2nn3hid26FinalizeSevenSixAxisSensorEv", ov_result_ok);
HOST_OVERRIDE("_ZN2nn3hid23StartSevenSixAxisSensorEv", ov_result_ok);
HOST_OVERRIDE("_ZN2nn3hid22StopSevenSixAxisSensorEv", ov_result_ok);
HOST_OVERRIDE("_ZN2nn3hid32ResetSevenSixAxisSensorTimestampEv", ov_result_ok);
HOST_OVERRIDE("_ZN2nn3hid27GetSevenSixAxisSensorStatesEPNS0_23SevenSixAxisSensorStateEi", ov_seven_states);
HOST_OVERRIDE("_ZN2nn3hid26IsSevenSixAxisSensorAtRestEv", ov_seven_at_rest);

// Debug pad (a development controller) and the touch screen of handheld mode: initialised, never touched.
// void GetDebugPadState(DebugPadState *): sampling number, attributes, buttons and both sticks, all zero (0x20 bytes)
static void ov_debug_pad_state(Cpu *c) { memset(arg_p(c, 0), 0, 0x20); }
// void GetTouchScreenState<1>(TouchScreenState<1> *): sampling number and a touch count of 0 lead the state
static void ov_touch_state(Cpu *c) { memset(arg_p(c, 0), 0, 0x10); }
HOST_OVERRIDE("_ZN2nn3hid18InitializeDebugPadEv", ov_nothing);
HOST_OVERRIDE("_ZN2nn3hid16GetDebugPadStateEPNS0_13DebugPadStateE", ov_debug_pad_state);
HOST_OVERRIDE("_ZN2nn3hid21InitializeTouchScreenEv", ov_nothing);
HOST_OVERRIDE("_ZN2nn3hid19GetTouchScreenStateILm1EEEvPNS0_16TouchScreenStateIXT_EEE", ov_touch_state);

// Joy-Con pairing: one host controller is one dual pad already.
HOST_OVERRIDE("_ZN2nn3hid23MergeSingleJoyAsDualJoyERKjS2_", ov_result_ok);
HOST_OVERRIDE("_ZN2nn3hid28SetNpadJoyAssignmentModeDualERKj", ov_nothing);

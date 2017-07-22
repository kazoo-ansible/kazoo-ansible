#!/usr/bin/python3

from ansible.module_utils.basic import *
import ansible.module_utils.urls
import json
import sup

EXPECTED_MEDIA = ['en-us/agent-already_logged_in', \
    'en-us/agent-invalid_choice', \
    'en-us/agent-logged_in', \
    'en-us/agent-logged_out', \
    'en-us/agent-not_call_center_agent', \
    'en-us/agent-pause', \
    'en-us/agent-resume', \
    'en-us/camper-deny', \
    'en-us/camper-queue', \
    'en-us/cf-disabled', \
    'en-us/cf-disabled_menu', \
    'en-us/cf-enabled_menu', \
    'en-us/cf-enter_number', \
    'en-us/cf-move-no_channel', \
    'en-us/cf-move-no_owner', \
    'en-us/cf-move-too_many_channels', \
    'en-us/cf-not_available', \
    'en-us/cf-now_forwarded_to', \
    'en-us/cf-unauthorized_call', \
    'en-us/conf-alone', \
    'en-us/conf-announce_your_name', \
    'en-us/conf-bad_conf', \
    'en-us/conf-bad_pin', \
    'en-us/conf-deaf', \
    'en-us/conf-enter_conf_number', \
    'en-us/conf-enter_conf_pin', \
    'en-us/conf-has_joined', \
    'en-us/conf-has_left', \
    'en-us/conf-joining_conference', \
    'en-us/conf-max_participants', \
    'en-us/conf-muted', \
    'en-us/conf-other_participants', \
    'en-us/conf-review', \
    'en-us/conf-single', \
    'en-us/conf-there_are', \
    'en-us/conf-too_many_attempts', \
    'en-us/conf-undeaf', \
    'en-us/conf-unmuted', \
    'en-us/conf-welcome', \
    'en-us/conf-your_announcment', \
    'en-us/cw-activated', \
    'en-us/cw-deactivated', \
    'en-us/cw-not_available', \
    'en-us/dir-confirm_menu', \
    'en-us/dir-enter_person', \
    'en-us/dir-enter_person_firstname', \
    'en-us/dir-enter_person_lastname', \
    'en-us/dir-first_name', \
    'en-us/dir-found', \
    'en-us/dir-invalid_key', \
    'en-us/dir-last_name', \
    'en-us/dir-letters_of_person_name', \
    'en-us/dir-no_more_results', \
    'en-us/dir-no_results_found', \
    'en-us/dir-result_menu', \
    'en-us/dir-result_number', \
    'en-us/dir-specify_minimum', \
    'en-us/disa-enter_pin', \
    'en-us/disa-invalid_extension', \
    'en-us/disa-invalid_pin', \
    'en-us/disa-retries_exceeded', \
    'en-us/dnd-activated', \
    'en-us/dnd-deactivated', \
    'en-us/dnd-not_available', \
    'en-us/dynamic-cid-enter_cid', \
    'en-us/dynamic-cid-invalid_using_default', \
    'en-us/eavesdrop-no_channels', \
    'en-us/fault-can_not_be_completed_as_dialed', \
    'en-us/fault-can_not_be_completed_at_this_time', \
    'en-us/fault-facility_trouble', \
    'en-us/hotdesk-abort', \
    'en-us/hotdesk-disabled', \
    'en-us/hotdesk-enter_id', \
    'en-us/hotdesk-enter_pin', \
    'en-us/hotdesk-invalid_entry', \
    'en-us/hotdesk-logged_in', \
    'en-us/hotdesk-logged_out', \
    'en-us/intercept-no_channels', \
    'en-us/intercept-no_users', \
    'en-us/ivr-group_confirm', \
    'en-us/menu-exit', \
    'en-us/menu-invalid_entry', \
    'en-us/menu-no_prompt', \
    'en-us/menu-return', \
    'en-us/menu-transferring_call', \
    'en-us/park-already_in_use', \
    'en-us/park-call_placed_in_spot', \
    'en-us/park-no_caller', \
    'en-us/pickup-no_channels', \
    'en-us/pickup-no_users', \
    'en-us/stepswitch-emergency_not_configured', \
    'en-us/temporal-marked_disabled', \
    'en-us/temporal-marked_enabled', \
    'en-us/temporal-marker_reset', \
    'en-us/temporal-menu', \
    'en-us/vm-abort', \
    'en-us/vm-deleted', \
    'en-us/vm-enter_forward_id', \
    'en-us/vm-enter_id', \
    'en-us/vm-enter_new_pin', \
    'en-us/vm-enter_new_pin_confirm', \
    'en-us/vm-enter_pass', \
    'en-us/vm-fail_auth', \
    'en-us/vm-forward_abort', \
    'en-us/vm-goodbye', \
    'en-us/vm-greeting_intro', \
    'en-us/vm-mailbox_full', \
    'en-us/vm-main_menu', \
    'en-us/vm-main_menu_not_configurable', \
    'en-us/vm-message_forwarding', \
    'en-us/vm-message_menu', \
    'en-us/vm-message_number', \
    'en-us/vm-new_messages', \
    'en-us/vm-no_access', \
    'en-us/vm-no_messages', \
    'en-us/vm-not_available', \
    'en-us/vm-not_available_no_voicemail', \
    'en-us/vm-person', \
    'en-us/vm-person_not_available', \
    'en-us/vm-pin_invalid', \
    'en-us/vm-pin_set', \
    'en-us/vm-received', \
    'en-us/vm-record_greeting', \
    'en-us/vm-record_message', \
    'en-us/vm-record_name', \
    'en-us/vm-record_temp_greeting', \
    'en-us/vm-recording_saved', \
    'en-us/vm-recording_to_short', \
    'en-us/vm-review_recording', \
    'en-us/vm-saved', \
    'en-us/vm-saved_message', \
    'en-us/vm-saved_messages', \
    'en-us/vm-settings_menu', \
    'en-us/vm-setup_complete', \
    'en-us/vm-setup_intro', \
    'en-us/vm-setup_rec_greeting', \
    'en-us/vm-thank_you', \
    'en-us/vm-you_have']

open_url = ansible.module_utils.urls.open_url

def main():
    module = AnsibleModule(
        argument_spec = dict(
            erlang_cookie = dict(required=True, type='str')
        ),
        supports_check_mode = True
    )

    try:
        response = open_url('http://localhost:15984/system_media/_all_docs')
        media = json.loads(response.read())
    except Exception as ex:
        module.fail_json(msg=str(ex))

    media = [row['id'] for row in media['rows']]

    import_needed = not set(EXPECTED_MEDIA).issubset(set(media))

    if not module.check_mode and import_needed:
        sup.import_media(module.params['erlang_cookie'])

    module.exit_json(changed=import_needed)

if __name__ == '__main__':
    main()


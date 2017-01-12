from business_rules.manager.action_manager import BaseActionManager


def test_use_base_action_manager():
    action_result = 'action result'
    with BaseActionManager(None, None, None, None, None) as action_manager:
        assert action_manager is not None
        action_manager.result = action_result

    assert action_manager.result is not None

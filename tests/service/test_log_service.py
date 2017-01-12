from mock import Mock

from business_rules.service.audit_service import AuditService


def test_constructor():
    audit_service = AuditService()
    assert audit_service is not None


def test_log_rule():
    audit_service = AuditService()
    audit_service.logger = Mock()

    audit_service.log_rule(None, None, None, None, None)

    audit_service.logger.info.assert_called_once()

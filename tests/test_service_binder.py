'''Tests for Maitre and Waiter classes'''
from unittest import mock

import pytest
from cli_talker.service_binder import BaseWaiter, Maitre, RESTWaiter


def test_maitre_raises_type_exception():
    """Check if a incomplete dict raises AtributeError"""
    porder = {}
    maitre = Maitre()
    with pytest.raises(AttributeError):
        maitre.process_order(porder)


def test_maitre_raises_method_exception():
    """Check if no waiter dict raises AtributeError"""
    porder = {'type': 'base'}
    maitre = Maitre()
    with pytest.raises(KeyError):
        maitre.process_order(porder)


def test_maitre_waiter():
    """Check if a complete dict instantiates OK"""
    order_base = {'type': 'base'}
    order_dict = {'type': 'dict'}
    maitre = Maitre()
    maitre.add_waiter({'dict': dict,
                       'base': BaseWaiter})
    test_waiter = maitre.process_order(order_base)
    assert isinstance(test_waiter, BaseWaiter)
    test_waiter = maitre.process_order(order_dict)
    assert isinstance(test_waiter, dict)
    assert not isinstance(test_waiter, BaseWaiter)


def test_waiter_method_exception():
    """Check correct Exception if no method informed"""
    maitre = Maitre()
    maitre.add_waiter({'base': BaseWaiter})
    order_base = {'type': 'base'}
    test_waiter = maitre.process_order(order_base)
    order = {}
    with pytest.raises(AttributeError):
        assert test_waiter.process_order(order)
    order = {'method': 'GET'}
    with pytest.raises(AttributeError):
        assert test_waiter.process_order(order)


def test_waiter_method():
    """Check if a complete dict instantiates OK"""
    maitre = Maitre()
    maitre.add_waiter({'base': BaseWaiter})
    order_base = {'type': 'base'}
    test_waiter = maitre.process_order(order_base)
    order = {'method': 'GET', 'resource': 'url'}
    assert test_waiter.process_order(order) == test_waiter.get_method
    order = {'method': 'POST', 'resource': 'url'}
    assert test_waiter.process_order(order) == test_waiter.post_method
    order = {'method': 'PUT', 'resource': 'url'}
    assert test_waiter.process_order(order) == test_waiter.put_method
    order = {'method': 'DELETE', 'resource': 'url'}
    assert test_waiter.process_order(order) == test_waiter.delete_method


@mock.patch('cli_talker.service_binder.requests')
def test_RESTWaiter_get_success(requests):
    requests.get.return_value.status_code = 200
    requests.get.return_value.text = 'mocked'
    maitre = Maitre()
    maitre.add_waiter({'rest': RESTWaiter})
    order = {'type': 'rest', 'method': 'GET', 'resource': 'url'}
    test_waiter = maitre.process_order(order)
    text, error, status_code = test_waiter.process_order(order)
    assert status_code == 200
    assert text == 'mocked'
    assert error is None


@mock.patch('cli_talker.service_binder.requests')
def test_RESTWaiter_get_failure(requests):
    requests.get.return_value.status_code = 401
    requests.get.return_value.text = 'mocked'
    maitre = Maitre()
    maitre.add_waiter({'rest': RESTWaiter})
    order = {'type': 'rest', 'method': 'GET', 'resource': 'url'}
    test_waiter = maitre.process_order(order)
    text, error, status_code = test_waiter.process_order(order)
    assert status_code == 401
    assert text is None
    assert error is 'mocked'

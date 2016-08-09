#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

from cabot_alert_pagerduty.models import _service_alertable
# from mappers.MapperLocator import find_mapper, MapperLookupError

class TestServiceStatusChecks(unittest.TestCase):

    def setUp(self):
        pass

    def test_valid_mapping(self):
        """ Proper class is returned via qualified name string """

        # from mappers.BaseMapper import BaseMapper

        # base_mapper_name = 'mappers.BaseMapper.BaseMapper'

        # base_mapper = find_mapper(base_mapper_name)

        self.assertEqual(True, True)

    # def test_non_qualified_mapper_name(self):
    #     """ A mapper name that is not fully qualified results in an error """

    #     mapper_name = 'BaseMapper'

    #     with self.assertRaises(MapperLookupError) as error:
    #         find_mapper(mapper_name)

    #     err_message = 'Incomplete class name specified: BaseMapper'
    #     self.assertEqual(str(error.exception), err_message)

    # def test_invalid_mapper_module(self):
    #     """ Invalid module name generate error when attempting to load """

    #     mapper_name = 'mapperz.BaseMapper'

    #     with self.assertRaises(MapperLookupError) as error:
    #         find_mapper(mapper_name)

    #     err_message = 'mapperz module cannot be found for class BaseMapper'
    #     self.assertEqual(str(error.exception), err_message)

    # def test_invalid_mapper_class_name(self):
    #     """ Invalid class name generates error when attempting to load """

    #     mapper_name = 'mappers.BaseMapper.LOLWut'

    #     with self.assertRaises(MapperLookupError) as error:
    #         find_mapper(mapper_name)

    #     err_msg = 'LOLWut class cannot be found in module mappers.BaseMapper'
    #     self.assertEqual(str(error.exception), err_msg)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestServiceStatusChecks)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
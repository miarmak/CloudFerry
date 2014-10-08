# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.


import copy


SRC = "src"
DST = "dst"


class Cloud(object):

    def __init__(self, resources, position, config):
        self.resources = resources
        self.position = position
        self.config = config

        cloud_config = self.make_cloud_config(self.config, self.position)
        self.init_resources(cloud_config)

    @staticmethod
    def make_cloud_config(config, position):
        cloud_config = {}
        for k, v in config.migrate.iteritems():
            cloud_config[k] = v

        for k, v in getattr(config, position).iteritems():
            cloud_config[k] = v

        for k, v in config.import_rules.iteritems():
            cloud_config[k] = v

        return cloud_config

    @staticmethod
    def make_resource_config(config, position, cloud_config, resource_name):
        resource_config = copy.deepcopy(cloud_config)
        for k, v in getattr(config,
                            '%s_%s' % (position, resource_name)).iteritems():
            resource_config[k] = v

        return resource_config

    def init_resources(self, cloud_config):
        init_resources = {}

        identity_conf = self.make_resource_config(self.config, self.position,
                                                  cloud_config, 'identity')
        identity = self.resources['identity'](identity_conf)
        init_resources['identity'] = identity

        for resource in self.resources:
            if resource != 'identity':
                resource_config = self.make_resource_config(self.config,
                                                            self.position,
                                                            cloud_config,
                                                            resource)
                init_resources[resource] = self.resources[resource](
                    resource_config, identity)

        self.resources = init_resources

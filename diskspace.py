#!/usr/bin/env python3

# Copyright: (c) 2022, Andrew Heath <aheath1992@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import subprocess
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: diskspace

short_description: Module that checks disk space of a pertition/

version_add: "1.0.1"

description: This module checks provided partition(s) to see if they are over a set threshold.

options:
    partition:
        description: The partition that you wish to check.
        required: true
        type: str
    threshold:
        description: The threshold of the partition you are checking.
        required: true
        type: str

author:
    - Andrew Heath (@aheath1992)
'''

EXAMPLES = r'''
Check partition
- name: check partition size
  diskspace:
    partition: /
    threshold: 90
'''

def space(partition, threshold):
    df = subprocess.Popen(['df', '-h', partition], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        splitline[5] == partition
        if splitline[4][:-1] > threshold:
            return True
        else:
            return False

def main():
    fields = {
            "partition": {"required": True, "type": "str"},
            "threshold": {"required": True, "type": "str"}
            }
    module = AnsibleModule(argument_spec=fields)
    partition = module.params['partition']
    threshold = module.params['threshold']

    result = space(partition,threshold)

    if result == False:
        module.exit_json(changed=False, msg="Partition %s is below threshold %s" % (partition, threshold))
    else:
        module.fail_json(msg="Partition %s is over threshold %s" % (partition, threshold))

if __name__ == '__main__':
    main()

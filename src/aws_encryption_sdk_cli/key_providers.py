# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Master key providers."""
import copy
from typing import Dict, List, Text, Union  # noqa pylint: disable=unused-import

from aws_encryption_sdk import KMSMasterKeyProvider
import botocore.session

from aws_encryption_sdk_cli.exceptions import BadUserArgumentError


def aws_kms_master_key_provider(**kwargs):
    # type: (**List[Union[Text, str]]) -> KMSMasterKeyProvider
    """Apply post-processing to transform ``KMSMasterKeyProvider``-specific values from CLI
    arguments to valid ``KMSMasterKeyProvider`` parameters, then call ``KMSMasterKeyprovider``
    with those parameters.

    :param dict kwargs: Named parameters collected from CLI arguments as prepared
        in aws_encryption_sdk_cli.internal.master_key_parsing._parse_master_key_providers_from_args
    :rtype: aws_encryption_sdk.key_providers.kms.KMSMasterKeyProvider
    """
    kwargs = copy.deepcopy(kwargs)
    try:
        profile_name = kwargs.pop('profile')
        if len(profile_name) != 1:
            raise BadUserArgumentError(
                'Only one profile may be specified per master key provider configuration. {} provided.'.format(
                    len(profile_name)
                )
            )
        kwargs['botocore_session'] = botocore.session.Session(profile=profile_name[0])
    except KeyError:
        pass
    try:
        region_name = kwargs.pop('region')
        if len(region_name) != 1:
            raise BadUserArgumentError(
                'Only one region may be specified per master key provider configuration. {} provided.'.format(
                    len(region_name)
                )
            )
        kwargs['region_names'] = region_name
    except KeyError:
        pass
    return KMSMasterKeyProvider(**kwargs)
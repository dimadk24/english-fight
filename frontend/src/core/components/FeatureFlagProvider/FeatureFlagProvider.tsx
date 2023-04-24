import React from 'react'
import { SplitClient, SplitFactory } from '@splitsoftware/splitio-react'
import SplitIO from '@splitsoftware/splitio/types/splitio'
import { Utils } from '../../../utils/Utils'
import { FeatureFlagService } from '../../FeatureFlagService'
import { useUserQuery } from '../WithUser/user-query'

type Props = {
  children: JSX.Element
}

const SPLIT_KEY = process.env.REACT_APP_SPLIT_KEY

function FeatureFlagProvider({ children }: Props): JSX.Element {
  const { data: user } = useUserQuery()

  const splitConfig: SplitIO.IBrowserSettings = {
    core: {
      authorizationKey: SPLIT_KEY,
      // https://github.com/splitio/react-client/issues/10
      key: 'anonymous',
    },
  }
  if (!Utils.isProductionMode) {
    splitConfig.core.authorizationKey = 'localhost'
    splitConfig.features = FeatureFlagService.getDevFeatureFlags()
  }
  const splitClientKey = user ? String(user.vkId) : 'anonymous'
  return (
    <SplitFactory config={splitConfig}>
      <SplitClient splitKey={splitClientKey}>{children}</SplitClient>
    </SplitFactory>
  )
}

export default FeatureFlagProvider

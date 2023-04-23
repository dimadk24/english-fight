import { useEffect } from 'react'
import { AppService } from '../../../AppService'
import { NOTIFICATIONS_STATUSES } from '../../../constants'
import { trackers } from '../../trackers/trackers'
import { UserInstance } from '../../user-model'
import { setUserData, useUserQuery } from './user-query'

type Props = {
  children({
    user,
    loadingUser,
    setUser,
  }: {
    user: UserInstance | null
    loadingUser: boolean
    setUser(user: UserInstance): void
  }): JSX.Element
}

function WithUser({ children }: Props): JSX.Element {
  const { isLoading, isSuccess, data: user } = useUserQuery()

  const userId = isSuccess && user.id
  const userVkId = isSuccess && user.vkId
  const userNotificationStatus = isSuccess && user.notificationsStatus

  useEffect(() => {
    const markNotificationsBlockedIfUserBlockedOnVkSide = async () => {
      if (
        userNotificationStatus === NOTIFICATIONS_STATUSES.ALLOW &&
        !AppService.areNotificationsEnabledOnVkSide
      ) {
        setUserData(await AppService.blockNotifications())
      }
    }

    if (isSuccess) {
      markNotificationsBlockedIfUserBlockedOnVkSide()
    }
  }, [isSuccess, userNotificationStatus])

  useEffect(() => {
    if (isSuccess) trackers.identify(userId, userVkId)
  }, [isSuccess, userId, userVkId])

  return children({
    user,
    loadingUser: isLoading,
    setUser: setUserData,
  })
}

export { WithUser }

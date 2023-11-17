import React, { useState } from 'react'
import Cell from '@vkontakte/vkui/dist/components/Cell/Cell'
import Counter from '@vkontakte/vkui/dist/components/Counter/Counter'
import Group from '@vkontakte/vkui/dist/components/Group/Group'
import Header from '@vkontakte/vkui/dist/components/Header/Header'
import Button from '@vkontakte/vkui/dist/components/Button/Button'
import Icon24Replay from '@vkontakte/icons/dist/24/replay'
import { Card, CardGrid, Div } from '@vkontakte/vkui'
import { Icon24Cancel } from '@vkontakte/icons'
import PanelHeader from '../../helpers/PanelHeader'
import Loader from '../../helpers/Loader'
import { AppService } from '../../../AppService'
import { NOTIFICATIONS_STATUSES } from '../../../constants'
import { GameInstance } from '../../../models/game-model'
import HomeButton from '../../helpers/HomeButton'
import {
  setUserData,
  useUserQuery,
} from '../../../core/components/WithUser/user-query'
import './SingleplayerResults.css'

type Props = {
  onGoBack(): void
  onRetry(): void
  battle: GameInstance
}

function SingleplayerResults({
  onGoBack,
  battle = null,
  onRetry,
}: Props): JSX.Element {
  const { data: user } = useUserQuery()
  const { questions, points } = battle
  const correctAnswersNumber = questions.filter(({ isCorrect }) => isCorrect)
    .length
  const incorrectAnswersNumber = questions.length - correctAnswersNumber
  const [rejectedNotifications, setRejectedNotifications] = useState(false)
  const [loading, setLoading] = useState(false)

  const showNotificationsRequest =
    user.notificationsStatus === NOTIFICATIONS_STATUSES.TO_BE_REQUESTED

  const navigationButtons = (
    <div className="action-buttons-wrapper">
      <HomeButton onClick={onGoBack} />
      <Button onClick={onRetry} size="l" before={<Icon24Replay />}>
        Again
      </Button>
    </div>
  )

  async function allowNotifications() {
    if (loading) return
    setLoading(true)
    try {
      const updatedUser = await AppService.requestNotifications()
      setUserData(updatedUser)
      if (updatedUser.notificationsStatus === NOTIFICATIONS_STATUSES.BLOCK) {
        // if user clicked subscribe, but rejected in VK popup
        setRejectedNotifications(true)
      }
    } finally {
      setLoading(false)
    }
  }

  async function blockNotifications() {
    if (loading) return
    setLoading(true)
    try {
      setUserData(await AppService.blockNotifications())
      setRejectedNotifications(true)
    } finally {
      setLoading(false)
    }
  }

  const notificationRequest = (
    <CardGrid style={{ marginTop: '10px' }}>
      <Card size="l" style={{ padding: '10px' }}>
        <div className="notification-request-content">
          <span className="notification-request-header">
            Узнай первым об обновлениях - подпишись на уведомления!
          </span>
          <div className="notification-buttons-wrapper">
            <Button
              size="m"
              mode="commerce"
              className="notification-button"
              onClick={allowNotifications}
              disabled={loading}
            >
              Подписаться
            </Button>
            <Button
              size="m"
              mode="secondary"
              className="notification-button"
              onClick={blockNotifications}
              disabled={loading}
            >
              Не сейчас
            </Button>
          </div>
          <span className="notification-request-close">
            <Icon24Cancel onClick={blockNotifications} />
          </span>
          <span className="notification-request-subtext">
            Всегда можно отписаться на главном экране
          </span>
        </div>
      </Card>
    </CardGrid>
  )
  return (
    <>
      <PanelHeader text="Results" onBackButtonClick={onGoBack} />
      <Group header={<Header mode="secondary">Statistics</Header>}>
        <Cell
          indicator={<Counter mode="primary">{correctAnswersNumber}</Counter>}
        >
          Correct answers:
        </Cell>
        <Cell
          indicator={<Counter mode="primary">{incorrectAnswersNumber}</Counter>}
        >
          Wrong answers:
        </Cell>
        <Cell indicator={<Counter mode="primary">{points}</Counter>}>
          Points:
        </Cell>
      </Group>
      {!showNotificationsRequest && navigationButtons}
      {showNotificationsRequest && notificationRequest}
      {rejectedNotifications && (
        <Div className="subscribe-later">
        </Div>
      )}
      {loading && <Loader />}
    </>
  )
}

export default SingleplayerResults

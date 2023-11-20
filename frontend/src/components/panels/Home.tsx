import React, { useState } from 'react'
import Button from '@vkontakte/vkui/dist/components/Button/Button'
import Group from '@vkontakte/vkui/dist/components/Group/Group'
import Cell from '@vkontakte/vkui/dist/components/Cell/Cell'
import Div from '@vkontakte/vkui/dist/components/Div/Div'
import Avatar from '@vkontakte/vkui/dist/components/Avatar/Avatar'
import { Link, Switch } from '@vkontakte/vkui'
import { Icon28UserOutline, Icon28UsersOutline } from '@vkontakte/icons'
import PanelHeader from '../helpers/PanelHeader'
import { AppService } from '../../AppService'
import { UserInstance } from '../../core/user-model'
import Loader from '../helpers/Loader'
import { NOTIFICATIONS_STATUSES } from '../../constants'
import {
  setUserData,
  useUserQuery,
} from '../../core/components/WithUser/user-query'

type Props = {
  onStartSingleGame(): void
  onStartMultiplayerGame(): void
}

const connectDevLink = 'https://vk.me/english_clash'

const Home = ({
  onStartSingleGame,
  onStartMultiplayerGame,
}: Props): JSX.Element => {
  const { data: user } = useUserQuery()
  const [loading, setLoading] = useState(false)

  const onSwitchNotifications = async (event) => {
    const { checked: newChecked } = event.target
    setLoading(true)
    try {
      let updatedUser: UserInstance
      if (newChecked) {
        // need to enable
        updatedUser = await AppService.requestNotifications()
      } else {
        // need to disable
        updatedUser = await AppService.blockNotifications()
      }
      setUserData(updatedUser)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <PanelHeader text="English Clash" showBackButton={false} />
      {user && (
        <Group>
          <Cell
            before={user.photoUrl ? <Avatar src={user.photoUrl} /> : null}
            description={
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span>Score - {user.score}</span>{' '}
                <span>Place in the rating: {user.foreverRank}</span>
              </div>
            }
            multiline
            data-testid="user-info"
          >
            {`${user.firstName} ${user.lastName}`}
          </Cell>
        </Group>
      )}

      <Group>
        <Div>
          <Cell>
            <Button
              before={<Icon28UserOutline />}
              size="xl"
              onClick={onStartSingleGame}
              disabled={loading}
            >
              Start single game
            </Button>
          </Cell>
          <Cell>
            <Button
              before={<Icon28UsersOutline />}
              size="xl"
              onClick={onStartMultiplayerGame}
              disabled={loading}
              mode="secondary"
            >
              Play with a friend
            </Button>
          </Cell>
        </Div>
      </Group>

      {user && (
        <Group>
          <Cell
            multiline
            indicator={
              <Switch
                checked={
                  user.notificationsStatus === NOTIFICATIONS_STATUSES.ALLOW
                }
                onChange={onSwitchNotifications}
                disabled={loading}
              />
            }
          >
            Notifications about updates
          </Cell>
        </Group>
      )}
      <Group>
        <Cell>
          <Link href={connectDevLink} target="_blank">
            Contact a developer
          </Link>
        </Cell>
      </Group>
      {loading && <Loader />}
    </>
  )
}

export default Home

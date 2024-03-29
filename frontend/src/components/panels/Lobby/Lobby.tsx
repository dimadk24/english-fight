import React, { useState } from 'react'
import { Button, Div, Group, Input, Snackbar } from '@vkontakte/vkui'
import { Icon28CopyOutline, Icon28ShareExternalOutline } from '@vkontakte/icons'
import bridge from '@vkontakte/vk-bridge'
import { GameDefinitionInstance } from '../../../models/game-definition-model'
import { ApiService } from '../../../core/ApiService'
import PanelHeader from '../../helpers/PanelHeader'
import Loader from '../../helpers/Loader'
import './Lobby.css'

type Props = {
  gameDefinition?: GameDefinitionInstance
  onGoBack(): void
}

const VK_APP_URL = ApiService.removeTrailingSlash(
  process.env.REACT_APP_VK_APP_URL
)

function Lobby({ gameDefinition, onGoBack }: Props): JSX.Element {
  const [copiedToastVisible, setCopiedToastVisible] = useState(false)

  if (!gameDefinition)
    return (
      <>
        <PanelHeader text="Игра с друзьями" onBackButtonClick={onGoBack} />
        <Loader />
      </>
    )

  const inviteUrl = `${VK_APP_URL}#gid=${gameDefinition.id}`

  const copy = async (text: string) => {
    await bridge.send('VKWebAppCopyText', { text })
    setCopiedToastVisible(true)
  }
  const shareLink = async () => {
    try {
      await bridge.send('VKWebAppShare', { link: inviteUrl })
    } catch (e) {
      const isUserCancelled =
        e.error_type === 'client_error' &&
        e.error_data &&
        e.error_data.error_code === 4 &&
        e.error_data.error_reason === 'User denied'
      if (!isUserCancelled) {
        throw e
      }
    }
  }

  const onCloseToast = () => setCopiedToastVisible(false)

  return (
    <>
      <PanelHeader text="Игра с другом" onBackButtonClick={onGoBack} />
      <Group>
        <Div>
          <div className="method-wrapper">
            <div className="invite-help-text">
              Отправь другому человеку эту ссылку, чтобы он(а) присоединился к
              игре
            </div>
            <div className="input-wrapper">
              <Input className="invite-url-input" value={inviteUrl} readOnly />
              <Button
                onClick={() => copy(inviteUrl)}
                className="copy-button"
                before={<Icon28CopyOutline />}
              >
                <span className="button-subtitle">Скопировать</span>
              </Button>
              <Button
                onClick={shareLink}
                className="share-button"
                before={<Icon28ShareExternalOutline />}
              >
                <span className="button-subtitle">Поделиться</span>
              </Button>
            </div>
          </div>
          <div className="method-wrapper second-method">
            <div className="invite-help-text">
              Еще можно присоединиться по ID игры
            </div>
            <div className="input-wrapper">
              <Input
                className="invite-url-input"
                value={gameDefinition.id}
                readOnly
              />
              <Button
                onClick={() => copy(gameDefinition.id)}
                className="copy-button"
                before={<Icon28CopyOutline />}
              >
                <span className="button-subtitle">Скопировать</span>
              </Button>
            </div>
          </div>
          <div className="loader-wrapper">
            <Loader />
            <span className="loader-caption">
              Ожидаем подключения второго человека
            </span>
          </div>
          {copiedToastVisible && (
            <Snackbar onClose={onCloseToast} duration={3000}>
              Скопировано
            </Snackbar>
          )}
        </Div>
      </Group>
    </>
  )
}

export default Lobby

import React, { useState } from 'react'
import { Button, Div, Input } from '@vkontakte/vkui'
import PanelHeader from '../../helpers/PanelHeader'
import './JoinMultiplayerGame.css'

type Props = {
  onJoin(gameDefinitionId: string): void
  onBack(): void
}

function JoinMultiplayerGame({ onJoin, onBack }: Props): JSX.Element {
  const [gameId, setGameId] = useState<string>('')

  const onChangeJoinMultiplayerGameId = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setGameId(e.target.value)
  }

  const onSubmit = (e) => {
    e.preventDefault()
    onJoin(gameId)
  }

  return (
    <>
      <PanelHeader text="Присоединиться к игре" onBackButtonClick={onBack} />
      <Div>
        <div className="join-game-help-text">ID игры:</div>
        <form onSubmit={onSubmit}>
          <Input onChange={onChangeJoinMultiplayerGameId} />
          <Div>
            <Button type="submit" stretched size="xl" disabled={!gameId.trim()}>
              Присоединиться
            </Button>
          </Div>
        </form>
      </Div>
    </>
  )
}

export default JoinMultiplayerGame

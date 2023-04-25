import React from 'react'
import { Cell, Group, List } from '@vkontakte/vkui'
import PanelHeader from '../../helpers/PanelHeader'

type Props = {
  onCreateNew(): void
  onJoin(): void
  onGoBack(): void
}

function ChooseMultiplayerGameAction({
  onCreateNew,
  onJoin,
  onGoBack,
}: Props): JSX.Element {
  return (
    <>
      <PanelHeader text="Игра с другом" onBackButtonClick={onGoBack} />
      <Group>
        <List>
          <Cell onClick={onCreateNew} expandable>
            Начать новую игру
          </Cell>
          <Cell onClick={onJoin} expandable>
            Присоединиться к существующей
          </Cell>
        </List>
      </Group>
    </>
  )
}

export default ChooseMultiplayerGameAction

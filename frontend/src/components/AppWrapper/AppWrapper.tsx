import React, { useEffect, useState } from 'react'
import * as Sentry from '@sentry/react'
import Alert from '@vkontakte/vkui/dist/components/Alert/Alert'
import bridge from '@vkontakte/vk-bridge'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { WithUser } from '../../core/components/WithUser/WithUser'
import App from '../App/App'
import { Utils } from '../../utils/Utils'
import styles from './AppWrapper.module.css'
import { trackers } from '../../core/trackers/trackers'
import FeatureFlagProvider from '../../core/components/FeatureFlagProvider/FeatureFlagProvider'
import { Themes } from '../../constants'
import { ThemeContext } from '../../react-contexts/theme'
import { queryClient } from '../../react-query-client'

function AppWrapper(): JSX.Element {
  const [popout, setPopout] = useState<JSX.Element | null>(null)
  const [theme, setTheme] = useState<Themes>(Themes.bright_light)

  useEffect(() => {
    bridge.send('VKWebAppInit')
    bridge.subscribe(({ detail: { type, data } }) => {
      if (type === 'VKWebAppUpdateConfig') {
        // @ts-ignore
        setTheme(data.scheme || Themes.bright_light)
      }
    })
  }, [])

  useEffect(() => {
    const schemeAttribute = document.createAttribute('scheme')
    schemeAttribute.value = theme
    document.body.attributes.setNamedItem(schemeAttribute)
  }, [theme])

  useEffect(() => {
    if (Utils.isProductionMode) {
      Sentry.init({
        dsn: process.env.REACT_APP_SENTRY_DSN,
        beforeSend(event, hint) {
          if (event.exception) {
            const errorMessage =
              hint &&
              hint.originalException &&
              hint.originalException instanceof Error &&
              hint.originalException.message
                ? hint.originalException.message
                : ''
            setPopout(
              <Alert
                actions={[
                  {
                    mode: 'default',
                    title: 'ОК',
                    autoclose: true,
                  },
                ]}
                onClose={() => setPopout(null)}
              >
                <h2>Возникла ошибка =(</h2>
                {errorMessage && (
                  <p className={styles.errorMessage}>{errorMessage}</p>
                )}
                <p>Попробуй еще раз</p>
              </Alert>
            )
          }
          return event
        },
      })
    }
    trackers.init()
    trackers.reachGoal('open app')
  }, [])

  return (
    <QueryClientProvider client={queryClient}>
      <WithUser>
        <FeatureFlagProvider>
          <ThemeContext.Provider value={theme}>
            <App popout={popout} />
          </ThemeContext.Provider>
        </FeatureFlagProvider>
      </WithUser>
      {!Utils.isE2E && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  )
}

export default AppWrapper

import 'core-js/features/map'
import 'core-js/features/set'
import React from 'react'
import { render as renderReact } from 'react-dom'
import { Utils } from './utils/Utils'
import { ErrorBoundary } from './components/ErrorBoundary'
import AppWrapper from './components/AppWrapper/AppWrapper'

function render() {
  renderReact(
    <React.StrictMode>
      <ErrorBoundary>
        <AppWrapper />
      </ErrorBoundary>
    </React.StrictMode>,
    document.getElementById('root')
  )
}
render()

if (!Utils.isProductionMode) {
  if (module.hot) {
    module.hot.accept('./components/App/App', render)
  }

  if (!Utils.isE2E) import('./eruda')
}

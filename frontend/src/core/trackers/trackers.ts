import { Utils } from '../../utils/Utils'
import { LocalTracker } from './LocalTracker'
import { VkPixelTracker } from './VkPixelTracker'
import { MixpanelTracker } from './MixpanelTracker'

const registeredTrackers = Utils.isProductionMode
  ? [VkPixelTracker, MixpanelTracker]
  : [LocalTracker]

function call(method: string, ...args: Array<unknown>) {
  registeredTrackers.forEach((tracker) => {
    if (
      tracker.AUTOMATIC_OPERATIONS[0] === '*' ||
      tracker.AUTOMATIC_OPERATIONS.includes(method)
    )
      tracker[method](...args)
  })
}

export const trackers = {
  identify(id: number, vkId: number): void {
    call('identify', id, vkId)
  },

  init(): void {
    call('init')
  },

  reachGoal(name: string, params?: Record<string, unknown>): void {
    call('reachGoal', name, params)
  },
}

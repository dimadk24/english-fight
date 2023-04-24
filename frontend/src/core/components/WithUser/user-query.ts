/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { useQuery } from '@tanstack/react-query'
import { AppService } from '../../../AppService'
import { queryClient } from '../../../react-query-client'
import { UserInstance } from '../../user-model'

const userQueryKey = ['user']

export const useUserQuery = () => {
  return useQuery({
    queryKey: userQueryKey,
    queryFn: AppService.fetchUserData,
    staleTime: Infinity,
  })
}

export const setUserData = (user: UserInstance) => {
  return queryClient.setQueryData(userQueryKey, user)
}

export const invalidateUser = () =>
  queryClient.invalidateQueries({ queryKey: userQueryKey })

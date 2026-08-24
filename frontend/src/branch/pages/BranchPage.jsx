import React from 'react'
import { BranchHeader } from '../components/BranchHeader'
import { BranchBody } from '../components/BranchBody'

export const BranchPage = () => {
  return (
    <div className="h-full p-5">
      <BranchHeader />
      <BranchBody />
    </div>
  )
}

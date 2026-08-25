import { PersonnelHeader } from '../components/PersonnelHeader'
import { PersonnelBody } from '../components/PersonnelBody'
import { useGetAllBranches } from '../../branch/hooks/useGetAllBranches'

export const PersonnelPage = () => {
  const branchesQuery = useGetAllBranches()

  return (
    <div className="h-full p-5">
      <PersonnelHeader branchesQuery={branchesQuery} />
      <PersonnelBody branchesQuery={branchesQuery} />
    </div>
  )
}
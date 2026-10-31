import Loader from "../../base/loading/Loader";
import { useTimePolicies } from "../../meals/hooks/useTimePolicies";
import { useTimePolicyStore } from "../../meals/store/useTimePolicyStore";
import TimePolicyForm from "../components/TimePolicyForm";

export default function TimePolicyPage() {
  const policies = useTimePolicies();
  const isComplete = useTimePolicyStore((state) => state.isComplete);

  const signature = policies
    .map((policy) => `${policy.target_weekday}:${policy.cutoff_before}`)
    .sort()
    .join("|");

  return (
    <div className="w-full space-y-6">
      {!isComplete && <Loader fullscreen={false} size={12} />}
      {isComplete && <TimePolicyForm key={signature} policies={policies} />}
    </div>
  );
}

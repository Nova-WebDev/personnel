import { useState, type FormEvent } from "react";

import { getErrorMessage } from "../../auth/utils";
import type { TimePolicy } from "../../meals/types";
import { submitClass } from "../../organization/components/formStyles";
import { useSetTimePolicies } from "../hooks/useSetTimePolicies";
import {
  WEEK,
  decodeCutoff,
  encodeCutoff,
  type Deadline,
} from "../utils/cutoff";
import PolicyRow from "./PolicyRow";

type FormState = Record<string, Deadline>;

const DEFAULT_DEADLINE: Deadline = { daysBefore: 1, localMinutes: 12 * 60 };

function initialState(policies: TimePolicy[]): FormState {
  return Object.fromEntries(
    WEEK.map((day) => {
      const found = policies.find(
        (policy) => policy.target_weekday.toLowerCase() === day.key,
      );
      return [
        day.key,
        found === undefined
          ? DEFAULT_DEADLINE
          : decodeCutoff(found.cutoff_before),
      ];
    }),
  );
}

interface TimePolicyFormProps {
  policies: TimePolicy[];
}

export default function TimePolicyForm({ policies }: TimePolicyFormProps) {
  const save = useSetTimePolicies();
  const [initial] = useState(() => initialState(policies));
  const [state, setState] = useState<FormState>(initial);

  const hasAll = policies.length === WEEK.length;
  const dirty =
    !hasAll ||
    WEEK.some(
      (day) => encodeCutoff(state[day.key]) !== encodeCutoff(initial[day.key]),
    );

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!dirty || save.isPending) return;
    save.mutate(
      WEEK.map((day) => ({
        target_weekday: day.key,
        cutoff_before: encodeCutoff(state[day.key]),
      })),
    );
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <ul className="space-y-3">
        {WEEK.map((day) => (
          <PolicyRow
            key={day.key}
            day={day}
            value={state[day.key]}
            onChange={(value) =>
              setState((current) => ({ ...current, [day.key]: value }))
            }
          />
        ))}
      </ul>

      {save.error !== null && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(save.error, "ثبت سیاست زمانی ناموفق بود.")}
        </p>
      )}
      {save.isSuccess && !dirty && (
        <p className="text-sm text-emerald-600 dark:text-emerald-400">
          ذخیره شد.
        </p>
      )}

      <button
        type="submit"
        disabled={!dirty || save.isPending}
        className={`${submitClass} w-full flex-none`}
      >
        {save.isPending ? "در حال ثبت..." : "ثبت"}
      </button>
    </form>
  );
}

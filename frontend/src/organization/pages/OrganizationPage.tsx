import {
  faBuilding,
  faPlus,
  faSitemap,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

import Modal from "../../base/Modal";
import BranchForm from "../components/BranchForm";
import UnitForm from "../components/UnitForm";
import { useBranches } from "../hooks/useBranches";

type ActiveModal = "branch" | "unit" | null;

const primaryButton =
  "flex h-11 cursor-pointer items-center gap-2 rounded-lg bg-teal-600 px-5 text-sm font-medium text-white transition hover:bg-teal-700";
const secondaryButton =
  "flex h-11 cursor-pointer items-center gap-2 rounded-lg border border-teal-600 px-5 text-sm font-medium text-teal-700 transition hover:bg-teal-50 dark:border-teal-400/60 dark:text-teal-300 dark:hover:bg-teal-400/10";

export default function OrganizationPage() {
  const [active, setActive] = useState<ActiveModal>(null);
  const { branches } = useBranches();

  const close = () => setActive(null);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          onClick={() => setActive("branch")}
          className={primaryButton}
        >
          <FontAwesomeIcon icon={faPlus} />
          افزودن سازمان
        </button>
        <button
          type="button"
          onClick={() => setActive("unit")}
          className={secondaryButton}
        >
          <FontAwesomeIcon icon={faPlus} />
          افزودن واحد
        </button>
      </div>

      <Modal open={active === "branch"} title="افزودن سازمان" onClose={close}>
        <BranchForm onDone={close} />
      </Modal>

      <Modal open={active === "unit"} title="افزودن واحد" onClose={close}>
        <UnitForm branches={branches} onDone={close} />
      </Modal>
    </div>
  );
}

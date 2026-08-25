import { POSITION_OPTIONS } from "../../constants/positionOptions";

export function PositionCell({ position }) {
  const option = POSITION_OPTIONS.find((opt) => opt.value === position);
  return option ? option.label : "—";
}
export interface Unit {
  unit_id: string;
  unit_name: string;
}

export interface Branch {
  branch_id: string;
  branch_name: string;
  units: Unit[];
}

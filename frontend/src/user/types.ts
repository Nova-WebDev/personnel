export type PermissionLevel =
  | "admin"
  | "kitchen"
  | "group_manager"
  | "hr_manager";

export interface Scope {
  level: string;
  unit_id: string | null;
  unit_name: string | null;
  branch_id: string | null;
  branch_name: string | null;
}

export interface Me {
  id: string;
  phone: string;
  first_name: string;
  last_name: string;
  personnel_code: string | null;
  rfid_card_id: string | null;
  photo_path: string | null;
  is_blocked: boolean;
  created_at: string;
  unit_id: string | null;
  unit_name: string | null;
  branch_id: string | null;
  branch_name: string | null;
  scopes: Scope[];
}

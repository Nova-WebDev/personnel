export interface Personnel {
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
}

export interface PersonnelView extends Personnel {
  unit_name: string | null;
  branch_id: string | null;
  branch_name: string | null;
}

export interface CreatePersonnelInput {
  phone: string;
  first_name: string;
  last_name: string;
  unit_id: string;
  personnel_code: string;
  photo: File | null;
}

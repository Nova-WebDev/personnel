import api from "../../shared/lib/axios";
import axiosMultipart from "../../shared/lib/axiosMultipart";
import type { CreatePersonnelInput, Personnel } from "../types";

function toFormData(input: CreatePersonnelInput): FormData {
  const form = new FormData();
  form.append("phone", input.phone);
  form.append("first_name", input.first_name);
  form.append("last_name", input.last_name);
  form.append("unit_id", input.unit_id);
  if (input.personnel_code !== "")
    form.append("personnel_code", input.personnel_code);
  if (input.photo !== null) form.append("photo", input.photo);
  return form;
}

export function getPersonnel() {
  return api.get<Personnel[]>("/user/users");
}

export function createPersonnel(input: CreatePersonnelInput) {
  return axiosMultipart.post("/user/user", toFormData(input));
}

export function updatePersonnel(id: string, input: CreatePersonnelInput) {
  return axiosMultipart.patch(`/user/user/${id}`, toFormData(input));
}

export function setBlocked(id: string, isBlocked: boolean) {
  return api.patch(`/user/user/${id}/blocked-status`, {
    is_blocked: isBlocked,
  });
}

export function setRfid(id: string, rfidCardId: string) {
  return api.put(`/user/user/${id}/rfid`, { rfid_card_id: rfidCardId });
}

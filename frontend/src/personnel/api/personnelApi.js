import api from "../../shared/lib/axios";
import axiosMultipart from "../../shared/lib/axiosMultipart";

function buildPersonnelFormData({
  personnelId,
  firstName,
  lastName,
  branchId,
  unitId,
  position,
  file,
}) {
  const formData = new FormData();
  formData.append("personnel_id", personnelId);
  formData.append("first_name", firstName);
  formData.append("last_name", lastName);
  formData.append("branch_id", branchId);
  if (unitId !== null && unitId !== undefined) {
    formData.append("unit_id", unitId);
  }
  if (position !== null && position !== undefined) {
    formData.append("position", position);
  }
  if (file) {
    formData.append("file", file);
  }
  return formData;
}

export function createPersonnel(payload) {
  const formData = buildPersonnelFormData(payload);
  return axiosMultipart.post("/personnel/", formData);
}

export function updatePersonnel(personnelUuid, payload) {
  const formData = buildPersonnelFormData(payload);
  return axiosMultipart.put(`/personnel/${personnelUuid}`, formData);
}

export function setPersonnelBlockStatus(personnelUuid, isBlocked) {
  return api.patch(`/personnel/${personnelUuid}/block-status`, {
    is_blocked: isBlocked,
  });
}

export function getPersonnelPaginated({
  page = 1,
  limit = 20,
  search = null,
  orderBy = "created_at",
  descending = true,
} = {}) {
  return api.get("/personnel/", {
    params: {
      page,
      limit,
      search,
      order_by: orderBy,
      descending,
    },
  });
}

export function getPersonnelDetail(personnelUuid) {
  return api.get(`/personnel/${personnelUuid}`);
}

export function getPersonnelPhotoUrl(fileId) {
  return `${api.defaults.baseURL}/personnel/photo/${fileId}`;
}

export function getPersonnelQrCodeUrl(personnelUuid) {
  return `${api.defaults.baseURL}/personnel/${personnelUuid}/qr`;
}
import Swal from "sweetalert2";

export async function confirmDelete(
  isDark: boolean,
  subject: string,
): Promise<boolean> {
  const result = await Swal.fire({
    title: "حذف",
    text: `آیا از حذف «${subject}» مطمئن هستید؟`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "حذف",
    cancelButtonText: "انصراف",
    reverseButtons: true,
    focusCancel: true,
    background: isDark ? "#0f2a36" : "#ffffff",
    color: isDark ? "#e2e8f0" : "#0f172a",
    confirmButtonColor: "#dc2626",
    cancelButtonColor: isDark ? "#334155" : "#64748b",
    customClass: { popup: "rounded-2xl" },
  });
  return result.isConfirmed;
}

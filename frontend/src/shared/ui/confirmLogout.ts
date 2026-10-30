import Swal from "sweetalert2";

export async function confirmLogout(isDark: boolean): Promise<boolean> {
  const result = await Swal.fire({
    title: "خروج از حساب؟",
    text: "آیا مطمئن هستید که می‌خواهید خارج شوید؟",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "خروج",
    cancelButtonText: "انصراف",
    reverseButtons: true,
    focusCancel: true,
    background: isDark ? "#0f2a36" : "#ffffff",
    color: isDark ? "#e2e8f0" : "#0f172a",
    confirmButtonColor: "#dc2626",
    cancelButtonColor: isDark ? "#334155" : "#64748b",
    iconColor: "#14b8a6",
    customClass: { popup: "rounded-2xl" },
  });
  return result.isConfirmed;
}

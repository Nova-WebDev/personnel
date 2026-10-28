import {
  faBurger,
  faChartColumn,
  faClock,
  faCreditCard,
  faGauge,
  faRotate,
  faSitemap,
  faUser,
  faUserShield,
  faUsers,
  faUtensils,
  type IconDefinition,
} from "@fortawesome/free-solid-svg-icons";

import type { PermissionLevel } from "../../user/types";

export interface MenuItem {
  to: string;
  label: string;
  icon: IconDefinition;
  levels?: PermissionLevel[];
}

export interface MenuGroup {
  label: string;
  items: MenuItem[];
}

export const menuGroups: MenuGroup[] = [
  {
    label: "عمومی",
    items: [
      { to: "/meals", label: "رزرو غذا", icon: faUtensils },
      { to: "/profile", label: "پروفایل من", icon: faUser },
    ],
  },
  {
    label: "آشپزخانه",
    items: [
      {
        to: "/redeem",
        label: "تحویل غذا",
        icon: faCreditCard,
        levels: ["kitchen"],
      },
      {
        to: "/reports/day",
        label: "گزارش روز",
        icon: faChartColumn,
        levels: ["kitchen"],
      },
      {
        to: "/manage/meals",
        label: "غذاها",
        icon: faBurger,
        levels: ["kitchen"],
      },
    ],
  },
  {
    label: "منابع انسانی",
    items: [
      {
        to: "/personnel",
        label: "پرسنل",
        icon: faUsers,
        levels: ["hr_manager"],
      },
    ],
  },
  {
    label: "مدیریت",
    items: [
      {
        to: "/admin/dashboard",
        label: "داشبورد",
        icon: faGauge,
        levels: ["admin"],
      },
      {
        to: "/admin/organization",
        label: "ساختار سازمان",
        icon: faSitemap,
        levels: ["admin"],
      },
      {
        to: "/admin/access",
        label: "کاربران و دسترسی",
        icon: faUserShield,
        levels: ["admin"],
      },
      {
        to: "/admin/time-policy",
        label: "سیاست زمانی",
        icon: faClock,
        levels: ["admin"],
      },
      {
        to: "/admin/meal-cycle",
        label: "چرخه غذا",
        icon: faRotate,
        levels: ["admin"],
      },
    ],
  },
];

import {
  faBurger,
  faChartColumn,
  faClock,
  faCreditCard,
  faGauge,
  faHouse,
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
  id: string;
  label: string;
  icon: IconDefinition;
  items: MenuItem[];
}

export const topItems: MenuItem[] = [
  { to: "/", label: "خانه", icon: faHouse },
  { to: "/profile", label: "پروفایل من", icon: faUser },
];

export const menuGroups: MenuGroup[] = [
  {
    id: "reports",
    label: "گزارش‌ها",
    icon: faChartColumn,
    items: [
      {
        to: "/admin/dashboard",
        label: "داشبورد",
        icon: faGauge,
        levels: ["admin"],
      },
      {
        to: "/reports/day",
        label: "گزارش روز",
        icon: faChartColumn,
        levels: ["kitchen"],
      },
    ],
  },
  {
    id: "food",
    label: "غذا",
    icon: faUtensils,
    items: [
      { to: "/meals", label: "رزرو غذا", icon: faUtensils },
      {
        to: "/redeem",
        label: "تحویل غذا",
        icon: faCreditCard,
        levels: ["kitchen"],
      },
      {
        to: "/manage/meals",
        label: "غذاها",
        icon: faBurger,
        levels: ["kitchen"],
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
  {
    id: "hr",
    label: "منابع انسانی",
    icon: faUsers,
    items: [
      {
        to: "/personnel",
        label: "پرسنل",
        icon: faUsers,
        levels: ["hr_manager"],
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
    ],
  },
];

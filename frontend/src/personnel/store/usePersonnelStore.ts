import { create } from "zustand";

import { useMeStore } from "../../user/store/useMeStore";
import type { Me } from "../../user/types";
import type { Personnel } from "../types";

interface PersonnelState {
  users: Record<string, Personnel>;
  rfidIndex: Record<string, string>;
  isComplete: boolean;
  setAll: (list: Personnel[]) => void;
  upsert: (user: Personnel) => void;
  upsertMe: (me: Me) => void;
  remove: (id: string) => void;
  invalidate: () => void;
}

function fromMe(me: Me): Personnel {
  return {
    id: me.id,
    phone: me.phone,
    first_name: me.first_name,
    last_name: me.last_name,
    personnel_code: me.personnel_code,
    rfid_card_id: me.rfid_card_id,
    photo_path: me.photo_path,
    is_blocked: me.is_blocked,
    created_at: me.created_at,
    unit_id: me.unit_id,
  };
}

function strip(user: Personnel): Personnel {
  return {
    id: user.id,
    phone: user.phone,
    first_name: user.first_name,
    last_name: user.last_name,
    personnel_code: user.personnel_code,
    rfid_card_id: user.rfid_card_id,
    photo_path: user.photo_path,
    is_blocked: user.is_blocked,
    created_at: user.created_at,
    unit_id: user.unit_id,
  };
}

function buildRfidIndex(
  users: Record<string, Personnel>,
): Record<string, string> {
  const index: Record<string, string> = {};
  for (const user of Object.values(users)) {
    if (user.rfid_card_id !== null)
      index[user.rfid_card_id.toUpperCase()] = user.id;
  }
  return index;
}

export const usePersonnelStore = create<PersonnelState>((set) => ({
  users: {},
  rfidIndex: {},
  isComplete: false,
  setAll: (list) =>
    set((state) => {
      const merged: Record<string, Personnel> = Object.fromEntries(
        list.map((user) => [user.id, strip(user)]),
      );
      for (const [id, user] of Object.entries(state.users)) {
        if (merged[id] === undefined) merged[id] = user;
      }
      return {
        users: merged,
        rfidIndex: buildRfidIndex(merged),
        isComplete: true,
      };
    }),
  upsert: (user) => {
    set((state) => {
      const users = { ...state.users, [user.id]: strip(user) };
      return { users, rfidIndex: buildRfidIndex(users) };
    });

    const { me, setMe } = useMeStore.getState();
    if (me !== null && me.id === user.id) {
      setMe({ ...me, ...strip(user) });
    }
  },
  upsertMe: (me) =>
    set((state) => {
      const users = {
        ...state.users,
        [me.id]: { ...state.users[me.id], ...fromMe(me) },
      };
      return { users, rfidIndex: buildRfidIndex(users) };
    }),
  remove: (id) =>
    set((state) => {
      const users = { ...state.users };
      delete users[id];
      return { users, rfidIndex: buildRfidIndex(users) };
    }),
  invalidate: () => set({ isComplete: false }),
}));

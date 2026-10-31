import { useMutation } from "@tanstack/react-query";

import { setRfid } from "../api";
import { usePersonnelStore } from "../store/usePersonnelStore";

export function useSetRfid() {
  return useMutation({
    mutationFn: ({ id, rfid }: { id: string; rfid: string }) =>
      setRfid(id, rfid),
    onSuccess: (_data, { id, rfid }) => {
      const { users, upsert } = usePersonnelStore.getState();
      const user = users[id];
      if (user !== undefined) upsert({ ...user, rfid_card_id: rfid });
    },
  });
}

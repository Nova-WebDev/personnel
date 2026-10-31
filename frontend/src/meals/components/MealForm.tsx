import { faCamera, faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  useEffect,
  useRef,
  useState,
  type ChangeEvent,
  type FormEvent,
} from "react";

import { getErrorMessage } from "../../auth/utils";
import {
  cancelClass,
  fieldClass,
  submitClass,
} from "../../organization/components/formStyles";
import DefaultMealImage from "../../shared/ui/DefaultMealImage";
import { useCreateMeal } from "../hooks/useCreateMeal";
import { useUpdateMeal } from "../hooks/useUpdateMeal";
import type { Meal } from "../types";

const labelClass = "mb-1.5 block text-sm text-gray-600 dark:text-gray-300";
const imageClass =
  "h-full w-full rounded-2xl ring-2 ring-teal-500/40 transition group-hover:ring-teal-500";

interface MealFormProps {
  initial?: Meal;
  onDone: () => void;
}

export default function MealForm({ initial, onDone }: MealFormProps) {
  const create = useCreateMeal();
  const update = useUpdateMeal();
  const mutation = initial === undefined ? create : update;
  const fileInput = useRef<HTMLInputElement>(null);

  const [title, setTitle] = useState(initial?.title ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [photo, setPhoto] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [currentFailed, setCurrentFailed] = useState(false);

  useEffect(() => {
    if (photo === null) {
      setPreview(null);
      return;
    }
    const url = URL.createObjectURL(photo);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [photo]);

  const currentPhoto =
    initial !== undefined && initial.photo_path !== null && !currentFailed
      ? `/api/meals/meal/${initial.id}/photo`
      : null;
  const shownPhoto = preview ?? currentPhoto;
  const canSubmit = title.trim() !== "" && !mutation.isPending;

  const handlePhoto = (event: ChangeEvent<HTMLInputElement>) => {
    setPhoto(event.target.files?.[0] ?? null);
  };

  const clearPhoto = () => {
    setPhoto(null);
    if (fileInput.current !== null) fileInput.current.value = "";
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!canSubmit) return;

    const input = {
      title: title.trim(),
      description: description.trim(),
      photo,
    };

    if (initial === undefined) create.mutate(input, { onSuccess: onDone });
    else update.mutate({ id: initial.id, input }, { onSuccess: onDone });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-h-[75vh] space-y-4 overflow-y-auto p-4"
    >
      <div className="flex flex-col items-center gap-2">
        <button
          type="button"
          onClick={() => fileInput.current?.click()}
          aria-label="انتخاب عکس"
          className="group relative h-32 w-32 cursor-pointer"
        >
          {shownPhoto === null ? (
            <DefaultMealImage className={imageClass} />
          ) : (
            <img
              src={shownPhoto}
              alt=""
              onError={() => setCurrentFailed(true)}
              className={`${imageClass} object-cover`}
            />
          )}
          <span className="absolute -bottom-2 -end-2 flex h-9 w-9 items-center justify-center rounded-xl bg-teal-600 text-white shadow-md transition group-hover:bg-teal-700">
            <FontAwesomeIcon icon={faCamera} />
          </span>
        </button>

        <input
          ref={fileInput}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          onChange={handlePhoto}
          className="hidden"
        />

        {photo !== null && (
          <button
            type="button"
            onClick={clearPhoto}
            className="flex cursor-pointer items-center gap-1.5 text-xs text-red-600 hover:underline dark:text-red-400"
          >
            <FontAwesomeIcon icon={faXmark} />
            حذف عکس انتخاب‌شده
          </button>
        )}
      </div>

      <div>
        <label htmlFor="meal-title" className={labelClass}>
          نام غذا
        </label>
        <input
          id="meal-title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          maxLength={100}
          className={fieldClass}
        />
      </div>

      <div>
        <label htmlFor="meal-description" className={labelClass}>
          توضیحات (اختیاری)
        </label>
        <textarea
          id="meal-description"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          maxLength={500}
          rows={3}
          className={`${fieldClass} resize-none`}
        />
      </div>

      {mutation.error !== null && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(mutation.error, "ثبت غذا ناموفق بود.")}
        </p>
      )}

      <div className="flex gap-3">
        <button type="button" onClick={onDone} className={cancelClass}>
          انصراف
        </button>
        <button type="submit" disabled={!canSubmit} className={submitClass}>
          {mutation.isPending ? "در حال ثبت..." : "ثبت"}
        </button>
      </div>
    </form>
  );
}

import { useMutation } from "@tanstack/react-query";

import { postRecommend, toRecommendRequest } from "../services/api";
import type { PreferenceFormValues, RecommendResponse } from "../types/api";

export function useRecommend() {
  return useMutation<RecommendResponse, Error, PreferenceFormValues>({
    mutationFn: (values) => postRecommend(toRecommendRequest(values)),
  });
}

"use client";

import * as React from "react";
import * as SwitchPrimitive from "@radix-ui/react-switch";

import { cn } from "./utils";

function Switch({
  className,
  ...props
}: React.ComponentProps<typeof SwitchPrimitive.Root>) {
  return (
    <SwitchPrimitive.Root
      data-slot="switch"
      className={cn(
        "peer inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border border-transparent transition-all outline-none disabled:cursor-not-allowed disabled:opacity-50",
        "data-[state=checked]:bg-black data-[state=unchecked]:bg-gray-300",
        "hover:data-[state=checked]:bg-gray-800 hover:data-[state=unchecked]:bg-gray-400",
        className,
      )}
      {...props}
    >
      <SwitchPrimitive.Thumb
        data-slot="switch-thumb"
        className={cn(
          "pointer-events-none block size-4 rounded-full shadow-sm transition-transform duration-200",
          "data-[state=checked]:translate-x-[18px] data-[state=unchecked]:translate-x-[2px]",
          "bg-white border border-gray-200"
        )}
        style={{
          boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)"
        }}
      />
    </SwitchPrimitive.Root>
  );
}

export { Switch };

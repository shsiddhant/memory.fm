// Generic Slider Selector with max and min values

import { Slider } from "@chakra-ui/react"
import { Tooltip } from "@/components/ui/tooltip"
import { useState } from "react"

export default function SliderSelector(
    { value, min, max, onValueChange }: {
        value: number
        min: number
        max: number
        onValueChange: (value: number) => void
    }
) {
    const [showTooltip, setShowTooltip] = useState(false)

    return (
        <Slider.Root
            defaultValue={[10]}
            value={[value]}
            min={min}
            max={max}
            minW={"300px"}
            variant={"solid"}
            colorPalette={"brand"}
            onValueChange={(details) => onValueChange(details.value[0])}
            onPointerEnter={() => setShowTooltip(true)}
            onPointerLeave={() => setShowTooltip(false)}
        >
            <Slider.ValueText />
            <Slider.Control>
                <Slider.Track colorPalette={"brand"}>
                    <Slider.Range />
                </Slider.Track>
                <Tooltip
                    open={showTooltip}
                    content={<Slider.ValueText />}
                    showArrow
                    contentProps={{ css: { "--tooltip-bg": "var(--chakra-colors-accent)" } }}
                >
          <Slider.Thumb index={0} />
        </Tooltip>
            </Slider.Control>
        </Slider.Root>
    )
}
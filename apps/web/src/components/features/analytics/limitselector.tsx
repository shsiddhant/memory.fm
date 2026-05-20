// Limit Selector: Max values to fetch from analytics API

import { Slider } from "@chakra-ui/react"
import { Tooltip } from "@/components/ui/tooltip"
import { useState } from "react"

export default function LimitSelector(
    { value, min, onLimitChange }: {
        value: number
        min: number
        onLimitChange: (value: number) => void
    }
) {
    const [showTooltip, setShowTooltip] = useState(false)

    return (
            <Slider.Root
                defaultValue={[10]}
                value={[value]}
                min={min}
                max={100}
                minW={{base: "200px", md: "300px"}}
                variant={"solid"}
                colorPalette={"brand"}
                onValueChange={(details) => onLimitChange(details.value[0])}
                onPointerEnter={() => setShowTooltip(true)}
                onPointerLeave={() => setShowTooltip(false)}
            >
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
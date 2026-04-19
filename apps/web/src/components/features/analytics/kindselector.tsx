import type { KindType } from "@/typing";
import { Tabs } from "@chakra-ui/react";


export default function KindSelector(
    { value, onKindChange }: {
        value: KindType
  onKindChange: (value: KindType) => void
    }
) {
    return (
            <Tabs.Root
                lazyMount
                unmountOnExit
                value={value}
                onValueChange={(details) => onKindChange(details.value as KindType)}
                variant="enclosed"
                defaultValue={"artist"}
                colorPalette={"brand"}
            >
                <Tabs.List>
                    <Tabs.Trigger value="artist">Artist</Tabs.Trigger>
                    <Tabs.Trigger value="album">Album</Tabs.Trigger>
                    <Tabs.Trigger value="track">Track</Tabs.Trigger>
                </Tabs.List>
                <Tabs.Content value="kind">

                </Tabs.Content>
            </Tabs.Root>
    )
}
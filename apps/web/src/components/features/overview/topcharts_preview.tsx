import { Box, Progress, Table } from "@chakra-ui/react";

interface TopChart {
    name: string,
    scrobbles: number
}

export default function TopChartsPreview(
    { kind, topCharts}: { kind: string, topCharts: TopChart[]}
) {

    const values = topCharts.map(chart => chart.scrobbles);
    const max = Math.max(...values);
    

    return (
        <Table.Root
            size="sm"
            width="sm"
        >
            <Table.Header>
                <Table.Row borderBottomWidth="1px">
                    <Table.ColumnHeader
                        color="fg.muted"
                        letterSpacing="wider"
                        fontSize="xs"
                    >
                        {kind.toUpperCase()}
                    </Table.ColumnHeader>
                    <Table.ColumnHeader
                        textAlign="end"
                        color="fg.muted"
                        letterSpacing="wider"
                        fontSize="xs"
                    >
                        SCROBBLES
                    </Table.ColumnHeader>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {topCharts.map((chart) => (
                    <Table.Row
                        key={chart.name}
                        borderBottomWidth={"2px"}
                        borderBottomColor={"bg"}
                    >
                        <Table.Cell py="3" fontWeight="500">
                            {chart.name}
                        </Table.Cell>
                        <Table.Cell py="3" textAlign="end" >
                            <Progress.Root
                                value={chart.scrobbles}
                                max={max}
                                colorPalette="brand"
                                variant="subtle"
                                shape="rounded"
                            >
                                <Box
                                    display="flex"
                                    justifyContent="space-between"
                                    mb="1"
                                >
                                    <Progress.ValueText fontVariantNumeric="tabular-nums">
                                        {chart.scrobbles}
                                    </Progress.ValueText>
                                </Box>
                                <Progress.Track height="6px">
                                    <Progress.Range />
                                </Progress.Track>
                            </Progress.Root>
                        </Table.Cell>
                    </Table.Row>
                ))}
            </Table.Body>
        </Table.Root>
    )
}
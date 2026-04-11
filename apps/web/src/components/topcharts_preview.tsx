import { Table } from "@chakra-ui/react";

interface TopChart {
    name: string,
    scrobbles: number
}

export default function TopChartsPreview(
    { kind, topCharts}: { kind: string, topCharts: TopChart[]}
) {
    return (
        <Table.Root size={"sm"}>
            <Table.Header>
                <Table.Row>
                    <Table.ColumnHeader>{ kind.toUpperCase() }</Table.ColumnHeader>
                    <Table.ColumnHeader textAlign={"end"}>SCROBBLES</Table.ColumnHeader>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {topCharts.map((chart) => (
                    <Table.Row key={chart.name}>
                        <Table.Cell>{chart.name}</Table.Cell>
                        <Table.Cell textAlign={"end"}>{chart.scrobbles}</Table.Cell>
                    </Table.Row>
                ))}
            </Table.Body>
        </Table.Root>
    )
}
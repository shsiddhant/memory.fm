// Period Selector: 7 Days, 30 Days, 365 Days, All Time, or Custom Date Range

import type { Dates, Mode, ModeOption } from "@/typing";
import {
  DatePicker,
  HStack,
  Portal,
  RadioGroup,
  Stack,
  type DateValue,
} from "@chakra-ui/react";
import { MdEditCalendar } from "react-icons/md";


function DateSelector(
  { label, value, onDateChange }: {
    label: string,
    value: DateValue[],
    onDateChange: (values: DateValue[]) => void
  }
) {
  return (
    <>
      <DatePicker.Root
        maxWidth={"20rem"}
        value={value}
        onValueChange={(details) => onDateChange(details.value)}
        variant="subtle"
        colorPalette="brand"
      >
        <DatePicker.Label >{label}</DatePicker.Label>
        <DatePicker.Control>
          <DatePicker.Input />
          <DatePicker.IndicatorGroup>
            <DatePicker.Trigger>
              <MdEditCalendar />
            </DatePicker.Trigger>
          </DatePicker.IndicatorGroup>
        </DatePicker.Control>
        <Portal>
          <DatePicker.Positioner>
            <DatePicker.Content colorPalette={"brand"}>
              <DatePicker.View view="day">
                <DatePicker.Header />
                <DatePicker.DayTable />
              </DatePicker.View>
              <DatePicker.View view="month">
                <DatePicker.Header />
                <DatePicker.MonthTable />
              </DatePicker.View>
              <DatePicker.View view="year">
                <DatePicker.Header />
                <DatePicker.YearTable />
              </DatePicker.View>
            </DatePicker.Content>
          </DatePicker.Positioner>
        </Portal>
      </DatePicker.Root>
    </>
  )
}

export default function PeriodSelector(
  { mode, onModeChange, customDates, onDatesChange }: {
    mode: Mode,
    onModeChange: (value: Mode) => void,
    customDates: Dates,
    onDatesChange: (key: keyof Dates, newValues: DateValue[]) => void,
  }
) {

  const modeOptions: ModeOption[] = [
    { value: 7, label: "7 Days" },
    { value: 30, label: "30 Days" },
    { value: 365, label: "365 Days" },
    { value: "all_time", label: "All Time" },
    { value: "custom", label: "Custom Date Range" },

  ];

  return (
    <>
      <RadioGroup.Root
        value={mode as string}
        onValueChange={(details) => onModeChange(details.value as Mode)}
        mb={"6"}
        colorPalette="brand"
      >
        <HStack>
          {modeOptions.map((item) => (
            <RadioGroup.Item key={item.value} value={item.value as string}>
              <RadioGroup.ItemHiddenInput />
              <RadioGroup.ItemIndicator />
              <RadioGroup.ItemText>{item.label}</RadioGroup.ItemText>
            </RadioGroup.Item>
          ))}
        </HStack>
      </RadioGroup.Root>
      {mode == "custom" && (
        <Stack direction={"row"} gap={"4"} p={"4"}>
          <DateSelector
            label="From"
            value={[customDates.from_ts]}
            onDateChange={(values) => onDatesChange("from_ts", values)}
          />
          <DateSelector
            label="To"
            value={[customDates.to_ts]}
            onDateChange={(values) => onDatesChange("to_ts", values)}
          />
        </Stack>
      )}
    </>
  )
}

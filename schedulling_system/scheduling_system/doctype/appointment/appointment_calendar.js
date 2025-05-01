frappe.views.calendar["Appointment"] = {
    field_map: {
        start: "start_date",
        end: "end_date",       
        id: "name",
        title: "client_name",         
        
    },
    options: {
        header: {
            left: "prev,next today",
            center: "title",
            right: "month,agendaWeek,agendaDay"
        }
    },
    get_events_method: "frappe.desk.calendar.get_events"
};
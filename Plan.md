## Events
Event driven, some of them (sent from server to client) are:
- Timeout: Connection timed out
- StatusOk: Request completed
- StatusFailed: Request failed
- ConnectionClosed: Closing connection
- ConnectionOpened: Opening connection

Client to server ones are:
- AdminJoined: An admin device has joined
- UserJoined: A user has joined (its telemetry time)
- AdminLeft: An admin device has left
- UserLeft: A user has left
- DBOpened: database successfully opened
- DBSuccess: database operation commited successfully
- DBFailed: operation errored in this case rollback to previous version

## Protocol
req: 
- type -> Otp | Database
- if Otp: number -> int
- if Database:
- query -> {"type": "C | R | U | D", "item": , "content": }

res:
- type -> Invalid | Success

__all__ = ["STATUS_RW", "STATUS_R", "STATUS_U", "JOB_STATUS_SUCCESS", "JOB_STATUS_ABORTED",
	"JOB_TYPE_RESET", "JOB_TYPE_SNAPSHOT", "JOB_TYPE_REINDEX", "JOB_TYPE_RESTORE"]

STATUS_RW = 'http://schemas.talis.com/2006/bigfoot/statuses#read-write'
STATUS_R = 'http://schemas.talis.com/2006/bigfoot/statuses#read-only'
STATUS_U = 'http://schemas.talis.com/2006/bigfoot/statuses#unavailable'

JOB_STATUS_SUCCESS = "http://schemas.talis.com/2006/bigfoot/configuration#success"
JOB_STATUS_ABORTED = "http://schemas.talis.com/2006/bigfoot/configuration#aborted"

JOB_TYPE_RESET = "http://schemas.talis.com/2006/bigfoot/configuration#ResetDataJob"
JOB_TYPE_SNAPSHOT = "http://schemas.talis.com/2006/bigfoot/configuration#SnapshotJob"
JOB_TYPE_REINDEX = "http://schemas.talis.com/2006/bigfoot/configuration#ReindexJob"
JOB_TYPE_RESTORE = "http://schemas.talis.com/2006/bigfoot/configuration#RestoreJob"

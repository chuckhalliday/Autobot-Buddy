resource "aws_cloudwatch_log_group" "autoadvisor-log-group" {
    name = "/ecs/autoadvisor"
    retention_in_days = var.log_retention_in_days
}
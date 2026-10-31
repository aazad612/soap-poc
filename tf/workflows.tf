resource "google_workflows_workflow" "countries_pipeline" {
  project         = google_project.soappoc.project_id
  name            = "ingest-all-countries-workflow"
  region          = var.region
  description     = "Sequentially triggers all 3 SOAP country ingestion Cloud Functions"
  service_account = google_service_account.soap_svc.email

  source_contents = <<-EOF
    main:
      steps:
        - init:
            assign:
              - pipeline_result: {}
        - step_1_first_countries_a_to_j:
            call: http.post
            args:
              url: ${google_cloudfunctions2_function.load_first_countries.service_config[0].uri}
              auth:
                type: OIDC
            result: res_1
        - step_2_second_countries_k_to_r:
            call: http.post
            args:
              url: ${google_cloudfunctions2_function.load_second_countries.service_config[0].uri}
              auth:
                type: OIDC
            result: res_2
        - step_3_third_countries_s_to_z:
            call: http.post
            args:
              url: ${google_cloudfunctions2_function.load_third_countries.service_config[0].uri}
              auth:
                type: OIDC
            result: res_3
        - return_summary:
            return:
              step_1_a_to_j: $${res_1.body}
              step_2_k_to_r: $${res_2.body}
              step_3_s_to_z: $${res_3.body}
  EOF

  depends_on = [
    google_project_service.enabled_apis,
    google_cloud_run_service_iam_member.invoker
  ]
}
